from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin", admin.site.urls),
    path("/adminpanel", include("adminpanel.urls")),
    path("", include("website.urls")),
]
