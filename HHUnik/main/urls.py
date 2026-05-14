from django.urls import path
from . import views
from vacancyAndCv.views import AllVacancyShow

app_name = 'main'
urlpatterns = [
    path("", AllVacancyShow.as_view(), name="index"),
    path("hr/", views.hrAccountPage.as_view(), name="hrAccountPage"),
    path("worker/", views.workerAccountPage.as_view(), name="workerAccountPage"),
]