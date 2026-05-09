from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("registr/", include("registration.urls")),
    path("", include("main.urls")),
    path("vacancy/", include("vacancyAndCv.urls")),
]

