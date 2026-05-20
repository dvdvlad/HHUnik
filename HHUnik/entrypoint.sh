#!/bin/sh
set -e

DEBUG_LOWER=$(echo "$DEBUG" | tr '[:upper:]' '[:lower:]')

echo "=== [Миграции] Проверка и применение изменений БД ==="
python manage.py migrate --noinput

echo "=== [Статика] Сборка статических файлов ==="
python manage.py collectstatic --noinput

if [ "$DEBUG_LOWER" = "true" ] || [ "$DEBUG_LOWER" = "1" ]; then
    echo "=== [DEBUG РЕЖИМ] Запуск встроенного сервера Django (runserver) ==="
    exec python manage.py runserver 0.0.0.0:8000
else
    echo "=== [ПРОДАКШН РЕЖИМ] Запуск боевого сервера Gunicorn (Gevent) ==="
    exec gunicorn HHUnik.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --worker-class gevent \
        --timeout 60 \
        --log-level "info" \
        --error-logfile -
fi
