from django.db import models
from django.conf import settings

class VacancyResponse(models.Model):
    vacancy = models.ForeignKey('vacancyAndCv.Vacancy', on_delete=models.CASCADE, related_name='responses')
    cv = models.ForeignKey('vacancyAndCv.CV', on_delete=models.CASCADE, related_name='applications')
    cv_embedding = models.JSONField(null=True, blank=True, help_text="Векторное представление резюме")
    match_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
