from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.urls import reverse
from django.views.generic.dates import models

class User(AbstractUser):
    isHR=models.BooleanField(default=True)# type: ignore


class slugMixin:
    slugSourceField = "title"
    slugUrlName = None
    def save(self, *args, **kwargs):
        if not self.slug:
            source_value = getattr(self, self.slugSourceField)
            self.slug = slugify(source_value)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(self.slugUrlName, kwargs={'slug': self.slug})
