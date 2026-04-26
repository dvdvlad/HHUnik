from django.db import models
from main.models import slugMixin


class Vacancy(slugMixin,models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)  # type: ignore
    slugSourceField = "title"
    slugUrlName = "vacancyAndCv:vacancyCard"
    slug = models.SlugField(max_length=255, unique=True, blank=True,db_index=True, verbose_name="URL")


class CV(slugMixin,models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)  # type: ignore


    slugSourceField = "title"
    slugUrlName = "cvCard"
    slug = models.SlugField(max_length=255, unique=True, blank=True,db_index=True, verbose_name="URL")
