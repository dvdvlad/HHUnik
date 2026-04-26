from django.urls import path
from . import views
app_name = 'main'  
urlpatterns = [
    path("", views.Main.as_view(), name="index"),
    path("account", views.hrAccountPage.as_view(), name="hrAccountPage"),
    path("worker", views.workerAccountPage.as_view(), name="workerAccountPage"),
]