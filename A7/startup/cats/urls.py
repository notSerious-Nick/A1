from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("Owner/<int:owner_id>/", views.owner),
    path("login/", views.login_user),
    path("add-cat/", views.add_cat),
    path("logout/", views.logout_owner, name="logout"),
    path("edit-cat/<int:cat_id>/", views.edit_cat, name="edit_cat"),
]
