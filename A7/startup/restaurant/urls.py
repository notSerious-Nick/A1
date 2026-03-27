from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="restaurant_dashboard"),
    path("orders-json/", views.orders_json, name="restaurant_orders_json"),
]