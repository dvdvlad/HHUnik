from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.urls import reverse
from django.db import models
import uuid


class User(AbstractUser):
    isHR = models.BooleanField(default=True,verbose_name="HR")  # type: ignore
    email = models.EmailField(max_length=254, verbose_name='Почта')
    phone = models.CharField(max_length=20, verbose_name='Телефон')

class slugMixin:
    slugSourceField = "title"
    slugUrlName = None
    def _generateUniqueSlug(self):
        source_value = getattr(self, self.slugSourceField)
        base_slug = slugify(source_value, allow_unicode=True)
        if not base_slug:
            base_slug = str(uuid.uuid4())[:8]
        slug = base_slug
        model_class = self.__class__
        qs = model_class.objects.filter(slug=slug)#type: ignore
        if self.pk:#type: ignore
            qs = qs.exclude(pk=self.pk)#type: ignore
        counter = 1
        while qs.exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            qs = model_class.objects.filter(slug=slug)#type: ignore
            if self.pk:#type: ignore
                qs = qs.exclude(pk=self.pk)#type: ignore
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generateUniqueSlug()
        super().save(*args, **kwargs)#type: ignore

    def get_absolute_url(self):
        return reverse(self.slugUrlName, kwargs={"slug": self.slug})