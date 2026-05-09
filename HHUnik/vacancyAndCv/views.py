from django.views.generic import CreateView, ListView, DetailView, View, TemplateView
from django.shortcuts import get_object_or_404, redirect
from vacancyAndCv.models import Vacancy, CV
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from cvAndVacancyMatching.embeding import  lmstudio,match
from cvAndVacancyMatching.models import VacancyResponse
from django.http import JsonResponse
import tempfile,os
import pymupdf4llm

class AddVacancy(LoginRequiredMixin, CreateView):
    model = Vacancy
    fields = ["title", "content", "is_published"]
    template_name = 'vacancy/addVacancy.html'
    success_url = reverse_lazy('main:hrAccountPage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddСV(LoginRequiredMixin, CreateView):
    model = CV
    fields = ["title", "content", "is_published"]
    template_name = 'vacancy/addCV.html'
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AllVacancyShow(LoginRequiredMixin, ListView):
    model = Vacancy
    template_name = 'vacancy/vacancyList.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Vacancy.objects.filter(is_published=True)#type: ignore


class VacancyDetailView(LoginRequiredMixin, DetailView):
    model = Vacancy
    template_name = 'vacancy/vacancyFull.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if not user.isHR:
            # Уже отправленные на эту вакансию
            sent_cv_ids = self.object.sendCV.filter(user=user).values_list('pk', flat=True)
            context['sent_cvs'] = CV.objects.filter(pk__in=sent_cv_ids)  #type: ignore
            # Показываем список доступных резюме только если ещё ничего не отправлено
            if not sent_cv_ids:
                context['user_cvs'] = CV.objects.filter(user=user, is_published=True)  #type: ignore
            else:
                context['user_cvs'] = CV.objects.none() #type: ignore
        else:
            # 1. Получаем отклики из промежуточной модели, отсортированные по баллам
            responses = VacancyResponse.objects.filter(
                vacancy=self.object
            ).select_related('cv', 'cv__user').order_by('-match_score')

            # 2. Формируем список резюме, "приклеивая" балл к каждому объекту
            sorted_cvs = []
            for r in responses:
                cv = r.cv
                cv.match_score = r.match_score  # Теперь у объекта CV есть атрибут match_score
                sorted_cvs.append(cv)

            # 3. Отдаем в шаблон под тем же именем, которое там уже используется
            context['all_sent_cvs'] = sorted_cvs            
            # context['all_sent_cvs'] = self.object.sendCV.select_related('user').order_by('-time_create')  # type: ignore
        return context


class SendCVView(LoginRequiredMixin, View):
    def post(self, request, slug):
        vacancy = get_object_or_404(Vacancy, slug=slug)
        cvId = request.POST.get('cv_id')
        #TODO: сделать получение адреса через setting.py
        endpoint = "http://localhost:1234/v1/embeddings" 
        embedder = lmstudio.lmStudioCompare(url=endpoint)
        matcher = match.cvMatcher(embedder)
        # Проверяем что резюме принадлежит текущему пользователю
        cv = get_object_or_404(CV, pk=cvId, user=request.user)
        embCv=embedder.getEmbedding(cv.content)
        embVacancy=embedder.getEmbedding(vacancy.content)
        # Запрещаем отправку, если пользователь уже откликнулся на эту вакансию
        if vacancy.sendCV.filter(user=request.user).exists():
            return redirect(vacancy.get_absolute_url())
        try:
            score = embedder.cosineCompare(embCv,embVacancy)
            VacancyResponse.objects.create(
                vacancy=vacancy,
                cv=cv,
                cv_embedding=embVacancy, 
                match_score=round(score, 4)
                )
        except Exception as e:
            print(f"Ошибка при расчете эмбеддингов: {e}")
        vacancy.sendCV.add(cv)
        
        return redirect(vacancy.get_absolute_url())


class WithdrawCVView(LoginRequiredMixin, View):
    def post(self, request, slug):
        vacancy = get_object_or_404(Vacancy, slug=slug)
        cv_id = request.POST.get('cv_id')
        # Проверяем что резюме принадлежит текущему пользователю
        cv = get_object_or_404(CV, pk=cv_id, user=request.user)
        vacancy.sendCV.remove(cv)
        return redirect(vacancy.get_absolute_url())


class CVDetailView(LoginRequiredMixin, DetailView):
    model = CV
    template_name = 'vacancy/cvFull.html'
    context_object_name = 'item'


class ToggleCVPublishView(LoginRequiredMixin, View):
    def post(self, request, slug):
        cv = get_object_or_404(CV, slug=slug)
        if cv.user != request.user:
            return HttpResponseForbidden()
        cv.is_published = not cv.is_published
        cv.save()
        return redirect('main:workerAccountPage')


class ToggleVacancyPublishView(LoginRequiredMixin, View):
    def post(self, request, slug):
        vacancy = get_object_or_404(Vacancy, slug=slug)
        if vacancy.user != request.user:
            return HttpResponseForbidden()
        vacancy.is_published = not vacancy.is_published
        vacancy.save()
        return redirect('main:hrAccountPage')



class BulkResumeUploadView(LoginRequiredMixin, TemplateView):
    # Указываем имя шаблона
    template_name = 'vacancy/uploadVacancy.html' 

    def post(self, request, *args, **kwargs):
            files = request.FILES.getlist("resumes")
            results = []
    
            if not files:
                return JsonResponse({"success": False, "error": "Файлы не получены"}, status=400)
    
            for uploaded_file in files:
                if not uploaded_file.name.endswith('.pdf'):
                    continue
    
                # 1. Создаем временный файл
                # delete=False нужен, чтобы файл не удалился сразу после закрытия дескриптора, 
                # так как pymupdf4llm будет открывать его по пути (path)
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                    for chunk in uploaded_file.chunks():
                        temp_file.write(chunk)
                    temp_path = temp_file.name
    
                try:
                    # 2. Конвертируем PDF в Markdown через pymupdf4llm
                    md_text = pymupdf4llm.to_markdown(temp_path)
    
                    # 3. Отделяем заголовок от контента
                    # Очищаем текст от лишних пробелов и делим на строки
                    lines = [line.strip() for line in md_text.split('\n') if line.strip()]
                    
                    if lines:
                        # Заголовок — первая строка (убираем символы Markdown #)
                        parsed_title = lines[0].lstrip('#').strip()
                        # Контент — всё остальное
                        parsed_content = "\n".join(lines[1:])
                    else:
                        parsed_title = uploaded_file.name
                        parsed_content = md_text
    
                    # 4. Сохраняем в БД
                    # slug сгенерируется автоматически благодаря вашему slugMixin
                    vacancy_obj = Vacancy.objects.create(
                        user=request.user,           # Привязка к текущему пользователю
                        title=parsed_title,          # Заголовок из PDF
                        content=parsed_content,      # Текст из PDF
                        is_published=True            # Или False, по вашему усмотрению
                    )
    
                    results.append({
                        "id": vacancy_obj.id,
                        "title": vacancy_obj.title,
                        "slug": vacancy_obj.slug
                    })
    
                except Exception as e:
                    # В продакшене лучше использовать logging
                    print(f"Ошибка обработки файла {uploaded_file.name}: {str(e)}")
                    continue 
                finally:
                    # Удаляем временный файл вручную
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
    
            return JsonResponse({
                "success": True,
                "count": len(results),
                "results": results
            })