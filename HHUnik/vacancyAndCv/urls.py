from django.urls import path
from . import views
app_name = 'vacancyAndCv'
urlpatterns = [
    path("vacancy", views.AddVacancy.as_view(), name="Vacancy"),
    path("cv", views.AddСV.as_view(), name="CV"),
]