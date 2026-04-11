from django.urls import path
from . import views
app_name = 'vacancyAndCv'
urlpatterns = [
    path("", views.AddPage.as_view(), name="Vacancy"),
]