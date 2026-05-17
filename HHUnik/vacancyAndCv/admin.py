from django.contrib import admin
from .models import Vacancy, CV, VacancyResponse

# Самый простой способ регистрации:
admin.site.register(Vacancy)
admin.site.register(CV)

# А для откликов можно сделать красивое отображение колонок, чтобы сразу видеть скор:
@admin.register(VacancyResponse)
class VacancyResponseAdmin(admin.ModelAdmin):
    # Какие поля показывать в виде таблицы в админке
    list_display = ('id', 'vacancy', 'cv', 'match_score', 'created_at')
    # Добавляем фильтрацию справа
    list_filter = ('vacancy', 'match_score')