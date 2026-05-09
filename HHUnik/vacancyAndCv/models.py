from django.db import models
from django.conf import settings
from main.models import slugMixin

class Vacancy(slugMixin,models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_vacancies', null=True, blank=True)  # type: ignore
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)  # type: ignore
    slugSourceField = "title"
    slugUrlName = "vacancyAndCv:vacancyCard"
    slug = models.SlugField(max_length=255, unique=True, blank=True,db_index=True, verbose_name="URL")
    sendCV = models.ManyToManyField('CV',related_name='vacancies')

class CV(slugMixin,models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cvs')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)  # type: ignore
    slugSourceField = "title"
    slugUrlName = "vacancyAndCv:cvCard"
    slug = models.SlugField(max_length=255, unique=True, blank=True,db_index=True, verbose_name="URL")
    