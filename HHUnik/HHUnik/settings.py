from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-*76dl_wk(88%*0^g9js+a9j=3x8pzo!5)!7^b)h7n86u8enk=q"
DEBUG = True
ALLOWED_HOSTS = []
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
    "cvAndVacancyMatching"
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
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
        "DIRS": [
            BASE_DIR/"templates"
            ],
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
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
LOGOUT_REDIRECT_URL = 'main:index'
LOGIN_REDIRECT_URL = 'main:index'
AUTH_USER_MODEL = 'main.User'
LOGIN_URL = 'registration:Login'

# ---------------------------------------------------------------------------
# LM Studio — локальный сервер эмбеддингов
# ---------------------------------------------------------------------------
# Базовый URL OpenAI-совместимого API LM Studio.
# Порт по умолчанию: 1234. Убедитесь, что сервер запущен в LM Studio
# (кнопка «Start Server» в разделе «Local Server»).
LM_STUDIO_BASE_URL = "http://localhost:1234/v1"

# Идентификатор модели эмбеддингов, загруженной в LM Studio.
# Укажите точное название из интерфейса, например:
#   "nomic-ai/nomic-embed-text-v1.5-GGUF"
#   "text-embedding-nomic-embed-text-v1.5"
# Если None — LM Studio использует текущую активную модель.
LM_STUDIO_EMBEDDING_MODEL = None

# Таймаут HTTP-запроса к LM Studio в секундах.
LM_STUDIO_TIMEOUT = 30