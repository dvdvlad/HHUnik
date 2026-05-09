from django.urls import path, re_path
from . import views

app_name = 'vacancyAndCv'
urlpatterns = [
    path("", views.AllVacancyShow.as_view(), name="listVacancy"),
    path("add/", views.AddVacancy.as_view(), name="Vacancy"),
    path("addPDF/", views.BulkResumeUploadView.as_view(), name="addVacancyPDF"),
    path("cv/", views.AddСV.as_view(), name="CV"),
    re_path(r'^cv/(?P<slug>[\w-]+)/$', views.CVDetailView.as_view(), name="cvCard"),
    re_path(r'^cv/(?P<slug>[\w-]+)/toggle-publish/$', views.ToggleCVPublishView.as_view(), name="toggleCVPublish"),
    re_path(r'^(?P<slug>[\w-]+)/toggle-publish/$', views.ToggleVacancyPublishView.as_view(), name="toggleVacancyPublish"),
    re_path(r'^(?P<slug>[\w-]+)/$', views.VacancyDetailView.as_view(), name="vacancyCard"),
    re_path(r'^(?P<slug>[\w-]+)/send-cv/$', views.SendCVView.as_view(), name="sendCV"),
    re_path(r'^(?P<slug>[\w-]+)/withdraw-cv/$', views.WithdrawCVView.as_view(), name="withdrawCV"),
]