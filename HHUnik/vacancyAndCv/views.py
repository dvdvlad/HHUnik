from django.views.generic import CreateView, ListView, DetailView, View
from django.shortcuts import get_object_or_404, redirect
from vacancyAndCv.models import Vacancy, CV
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class AddVacancy(LoginRequiredMixin, CreateView):
    model = Vacancy
    fields = ["title", "content", "is_published"]
    template_name = 'vacancy/addVacancy.html'
    success_url = reverse_lazy('main:index')


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
        return Vacancy.objects.filter(is_published=True)


class VacancyDetailView(LoginRequiredMixin, DetailView):
    model = Vacancy
    template_name = 'vacancy/vacancyFull.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if not user.isHR:
            # Все резюме пользователя
            user_cvs = CV.objects.filter(user=user, is_published=True)
            # Уже отправленные на эту вакансию
            sent_cv_ids = self.object.sendCV.filter(user=user).values_list('pk', flat=True)
            context['user_cvs'] = user_cvs.exclude(pk__in=sent_cv_ids)
            context['sent_cvs'] = CV.objects.filter(pk__in=sent_cv_ids)
        return context


class SendCVView(LoginRequiredMixin, View):
    def post(self, request, slug):
        vacancy = get_object_or_404(Vacancy, slug=slug)
        cv_id = request.POST.get('cv_id')
        # Проверяем что резюме принадлежит текущему пользователю
        cv = get_object_or_404(CV, pk=cv_id, user=request.user)
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