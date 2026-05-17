import os
from django.core.wsgi import get_wsgi_application

# === ДОБАВИТЬ ЭТИ СТРОЧКИ СТРОГО СВЕРХУ ===
try:
    from gevent import monkey
    monkey.patch_all()
except ImportError:
    pass
# =========================================

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HHUnik.settings")

application = get_wsgi_application()