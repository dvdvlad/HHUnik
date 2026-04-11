from django.views.generic.edit import CreateView
from vacancyAndCv.models import Vacancy
from django.urls import reverse_lazy
class AddPage(CreateView):
    model = Vacancy
    fields = '__all__'
    template_name = 'vacancy/addpage.html'
    success_url = reverse_lazy('/')
    extra_context = {
        'title': 'Добавление статьи',
    }
