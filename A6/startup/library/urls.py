from django.urls import path
from . import views

urlpatterns = [
    # Added for A6
    path("books/", views.books_list, name="books"),
    path("books/<str:isbn>/", views.book_detail, name="book_detail"),
    path("librarian/", views.librarian_dashboard, name="librarian"),

    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
