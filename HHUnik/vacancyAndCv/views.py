from django.views.generic import CreateView, ListView, DetailView, View, TemplateView
from django.shortcuts import get_object_or_404, redirect
from vacancyAndCv.models import Vacancy, CV, VacancyResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.html import strip_tags
from django.http import HttpResponseForbidden
from django import forms
from cvAndVacancyMatching.embeding import  lmstudio,match,yandex
from django.http import JsonResponse
import tempfile,os,re,pymupdf4llm


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ["title", "content", "is_published"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class AddVacancy(LoginRequiredMixin, CreateView):
    model = Vacancy
    form_class=VacancyForm
    template_name = 'vacancy/addVacancy.html'
    success_url = reverse_lazy('main:hrAccountPage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ["title", "content", "is_published"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class AddСV(LoginRequiredMixin, CreateView):
    model = CV
    form_class=CVForm
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
                sent_cv_ids = self.object.sendCV.filter(user=user).values_list('pk', flat=True)
                context['sent_cvs'] = CV.objects.filter(pk__in=sent_cv_ids)  #type: ignore
                if not sent_cv_ids:
                    context['user_cvs'] = CV.objects.filter(user=user, is_published=True)  #type: ignore
                else:
                    context['user_cvs'] = CV.objects.none() #type: ignore
            else:
                responses = VacancyResponse.objects.filter(
                    vacancy=self.object
                ).select_related('cv', 'cv__user').order_by('-match_score')
                raw_scores = [r.match_score for r in responses if r.match_score is not None]
                embedder = yandex.YandexCompare()
                percentages = embedder.get_human_percentage(raw_scores)
                sorted_cvs = []
                for r, percent in zip(responses, percentages):
                    cv = r.cv
                    cv.match_score = r.match_score  
                    cv.human_percentage = percent 
                    sorted_cvs.append(cv)
                if hasattr(embedder, 'close'):
                    embedder.close()
                sorted_cvs.sort(key=lambda x: x.human_percentage, reverse=True)
                context['all_sent_cvs'] = sorted_cvs
            return context
class SendCVView(LoginRequiredMixin, View):
    def clean_text(self,raw_text)->str:
        if not raw_text:
            return ""
        text = strip_tags(raw_text)
        text = re.sub(r'(Стр\.\s*\d+\s*из\s*\d+|Report content on this page|Стр\.\s*\d+)', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\s+', ' ', text)
        return text[:6000].strip()
    def post(self, request, slug):
        vacancy = get_object_or_404(Vacancy, slug=slug)
        cvId = request.POST.get('cv_id')
        embedder = yandex.YandexCompare()

        cv = get_object_or_404(CV, pk=cvId, user=request.user)

        if vacancy.sendCV.filter(user=request.user).exists():
            return redirect(vacancy.get_absolute_url())
        
        cleaned_cv = self.clean_text(cv.content)
        cleaned_vacancy = self.clean_text(vacancy.content)
        embCv = embedder.getEmbedding(self.clean_text(cv.content))
        embVacancy = embedder.getEmbedding(self.clean_text(vacancy.content),is_query=True)

        try:
            score = embedder.cosineCompare(embVacancy,embCv)
            # Создание записи в VacancyResponse автоматически создаст связь в vacancy.sendCV
            VacancyResponse.objects.create(
                vacancy=vacancy,
                cv=cv,
                cv_embedding=embCv, 
                match_score=score
            )
        except Exception as e:
            print(f"Ошибка при расчете эмбеддингов: {e}")
            VacancyResponse.objects.create(vacancy=vacancy, cv=cv, match_score=-1.0)
        finally:
            embedder.close()

        return redirect(vacancy.get_absolute_url())


class WithdrawCVView(LoginRequiredMixin, View):
    def post(self, request, slug):
        vacancy = get_object_or_404(Vacancy, slug=slug)
        cv_id = request.POST.get('cv_id')
        cv = get_object_or_404(CV, pk=cv_id, user=request.user)
        VacancyResponse.objects.filter(vacancy=vacancy, cv=cv).delete()

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
    template_name = 'vacancy/uploadVacancy.html'
    def post(self, request, *args, **kwargs):
            files = request.FILES.getlist("resumes")
            results = []

            if not files:
                return JsonResponse({"success": False, "error": "Файлы не получены"}, status=400)

            for uploaded_file in files:
                if not uploaded_file.name.endswith('.pdf'):
                    continue
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
                "count_uploaded": len(results),
                "results": results
            })
