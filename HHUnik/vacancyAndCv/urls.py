from django.urls import path
from . import views

app_name = 'vacancyAndCv'
urlpatterns = [
    path("vacancy", views.AddVacancy.as_view(), name="Vacancy"),
    path("", views.AllVacancyShow.as_view(), name="listVacancy"),
    path("<slug:slug>/", views.VacancyDetailView.as_view(), name="vacancyCard"),
    path("<slug:slug>/send-cv/", views.SendCVView.as_view(), name="sendCV"),
    path("<slug:slug>/withdraw-cv/", views.WithdrawCVView.as_view(), name="withdrawCV"),
    path("cv", views.AddСV.as_view(), name="CV"),
    path("cv/<slug:slug>/", views.CVDetailView.as_view(), name="cvCard"),
]