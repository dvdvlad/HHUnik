from django.views.generic.edit import CreateView
from vacancyAndCv.models import Vacancy, CV
from django.urls import reverse_lazy
class AddVacancy(CreateView):
    model = Vacancy
    fields = '__all__'
    template_name = 'vacancy/addVacancy.html'
    success_url = reverse_lazy('main:index')

class AddСV(CreateView):
    model = CV
    fields = '__all__'
    template_name = 'vacancy/addCV.html'
    success_url = reverse_lazy('main:index')
