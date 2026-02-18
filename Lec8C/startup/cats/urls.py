from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("author", views.author),
    path("<int:owner_id>/", views.detail, name="detail")
]
