import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 1. СНАЧАЛА ОБЪЯВЛЯЕМ КЛЮЧ И ДЕБАГ (В самом верху файла)
SECRET_KEY = os.environ.get('SECRET_KEY')
DEM= os.environ['DEMO']==True
DEBUG = os.environ.get('DEBUG', 'False')

# Если ключа нет в .env, выставляем безопасную заглушку для локальной разработки
if not SECRET_KEY:
    SECRET_KEY = 'local-secret-key-for-development-purposes-only-12345'

ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "registration",
    "main",
    "vacancyAndCv",
    "cvAndVacancyMatching",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "HHUnik.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "HHUnik.wsgi.application"

# База данных жестко завязана на переменные окружения из .env и docker-compose
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'hr_ai_db'),
        'USER': os.environ.get('DB_USER', 'hr_admin'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '123'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru-RU"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

if not DEBUG:
    print(DEBUG,SECRET_KEY)
    if 'local-secret' in SECRET_KEY:
        raise ValueError("Критическая ошибка: ПЕРЕМЕННАЯ SECRET_KEY НЕ ЗАДАНА В .ENV НА ПРОДАКШЕНЕ!")

    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1 localhost').split()

    # ВЫКЛЮЧАЕМ локальный HTTPS-редирект для тестов на 127.0.0.1
    # Когда выкатишь на реальный сервер за Nginx, вернешь True
    SECURE_SSL_REDIRECT = False

    # Отключаем принудительный SSL для куки-файлов на время локальных тестов
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

    # Сбрасываем HSTS в 0, чтобы браузер не блокировал HTTP-соединение на локалке
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
# Настройки статики (STATIC_ROOT меняем на изолированную папку, как обсуждали)
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "main" / "static",
]

LOGOUT_REDIRECT_URL = 'main:index'
LOGIN_REDIRECT_URL = 'main:index'
AUTH_USER_MODEL = 'main.User'
LOGIN_URL = 'registration:Login'
