from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.registration_form, name="registration_form"),
    path("events/", views.event_list, name="event_list"),
]
