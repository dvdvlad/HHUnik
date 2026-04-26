from django.urls import path
from . import views
app_name = 'vacancyAndCv'
urlpatterns = [
    path("vacancy", views.AddVacancy.as_view(), name="Vacancy"),
    path("", views.AllVacancyShow.as_view(), name="listVacancy"),
    path("<slug:slug>/", views.VacancyDetailView.as_view(), name="vacancyCard"),
    path("cv", views.AddСV.as_view(), name="CV"),
]
