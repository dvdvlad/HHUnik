from django.db import models
from django.conf import settings
from main.models import slugMixin

class Vacancy(slugMixin,models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_vacancies', null=True, blank=True)  # type: ignore
    title = models.CharField(max_length=255,verbose_name="Загаловок")
    content = models.TextField(blank=True,verbose_name="Резюме")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False,verbose_name="Опубликовать")  # type: ignore
    slugSourceField = "title"
    slugUrlName = "vacancyAndCv:vacancyCard"
    slug = models.SlugField(max_length=255, unique=True, blank=True,db_index=True, verbose_name="URL")
    sendCV = models.ManyToManyField('CV', through='VacancyResponse', related_name='sent_vacancies')
class CV(slugMixin,models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cvs')
    title = models.CharField(max_length=255,verbose_name="Загаловок")
    content = models.TextField(blank=True,verbose_name="Резюме")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False,verbose_name="Опубликовать")  # type: ignore
    slugSourceField = "title"
    slugUrlName = "vacancyAndCv:cvCard"
    slug = models.SlugField(max_length=255, unique=True, blank=True,db_index=True, verbose_name="URL")
    
    
class VacancyResponse(models.Model):
    vacancy = models.ForeignKey('vacancyAndCv.Vacancy', on_delete=models.CASCADE, related_name='responses')
    cv = models.ForeignKey('vacancyAndCv.CV', on_delete=models.CASCADE, related_name='applications')
    cv_embedding = models.JSONField(null=True, blank=True, help_text="Векторное представление резюме")
    match_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)