from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda r: redirect("books")), 
    path("library/", include("library.urls")),
    path("conferences/", include("conferences.urls")),
    path("cats/", include("cats.urls")),
    path("admin/", admin.site.urls),
]