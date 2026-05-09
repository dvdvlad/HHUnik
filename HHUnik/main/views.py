from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from vacancyAndCv.models import CV, Vacancy


class Main(TemplateView):
    template_name = "base.html"


class hrAccountPage(LoginRequiredMixin, TemplateView):
    template_name = "main/hrPage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.filter(user=self.request.user).order_by('-time_create')  # type: ignore
        return context


class workerAccountPage(LoginRequiredMixin, TemplateView):
    template_name = "main/workerPage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cvs'] = CV.objects.filter(user=self.request.user).order_by('-time_create')#type: ignore
        return context