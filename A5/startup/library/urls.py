from django.urls import path
from . import views

urlpatterns = [
    path("q1-authors/", views.q1_all_authors, name="q1_all_authors"),
    path("q2-books/", views.q2_all_books, name="q2_all_books"),
    path("q3-books-after/<int:year>/", views.q3_books_after_year, name="q3_books_after_year"),
    path("q4-books-by-author/<int:author_id>/", views.q4_books_by_author, name="q4_books_by_author"),
    path("q5-open-loans/", views.q5_open_loans, name="q5_open_loans"),
    path("q6-loans-due-before/", views.q6_loans_due_before, name="q6_loans_due_before"),
    path("q7-book/<str:isbn>/", views.q7_book_by_isbn, name="q7_book_by_isbn"),
    path("q8-stats/", views.q8_stats, name="q8_stats"),
]
