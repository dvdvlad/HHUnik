import os
from django.core.wsgi import get_wsgi_application

DEBUG_LOWER = os.environ.get('DEBUG', 'False').lower()

# Запускаем gevent ТОЛЬКО на продакшене (когда DEBUG=False)
if DEBUG_LOWER not in ('true', '1', 't'):
    try:
        from gevent import monkey
        monkey.patch_all()
    except ImportError:
        pass

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HHUnik.settings")

application = get_wsgi_application()