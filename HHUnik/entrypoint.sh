#!/bin/sh

# Выходим при любой ошибке
set -e

echo "=== [Миграции] Проверка и применение изменений БД ==="
python manage.py migrate --noinput

echo "=== [Статика] Сборка статических файлов для WhiteNoise ==="
python manage.py collectstatic --noinput

echo "=== [Продакшн] Запуск сервера Gunicorn с асинхронными воркерами Gevent ==="
exec gunicorn HHUnik.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --worker-class gevent \
    --timeout 60