from django.views.generic import CreateView, ListView,DetailView
from vacancyAndCv.models import Vacancy, CV
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
class AddVacancy(LoginRequiredMixin,CreateView):
    model = Vacancy
    fields = ["title","content","is_published"]
    template_name = 'vacancy/addVacancy.html'
    success_url = reverse_lazy('main:index')

class AddСV(LoginRequiredMixin,CreateView):
    model = CV
    fields = ["title","content","is_published"]
    template_name = 'vacancy/addCV.html'
    success_url = reverse_lazy('main:index')

class AllVacancyShow(LoginRequiredMixin,ListView):
    model = Vacancy
    template_name = 'vacancy/vacancyList.html'
    context_object_name = 'items'

class VacancyDetailView(LoginRequiredMixin,DetailView):
        model = Vacancy
        template_name = 'vacancy/vacancyFull.html' # Путь к шаблону
        context_object_name = 'item'
