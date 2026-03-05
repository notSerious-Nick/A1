from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Book, Loan, Borrower, Librarian

# Provided login and logout functionality
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse

def login_view(request):
    # Support "next" so @login_required redirects back after login
    next_url = request.GET.get("next") or request.POST.get("next") or reverse("books")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url)

        return render(request, "login.html", {
            "error": "Invalid username or password.",
            "next": next_url,
            "username": username,
        })

    return render(request, "login.html", {"next": next_url})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("books")
    return render(request, "logout.html")

def _borrower_for_user(user):
    if user is None or not user.is_authenticated:
        return None
    return Borrower.objects.filter(account=user).first()

def books_list(request):
    books = Book.objects.select_related("author").order_by("title")
    return render(request, "books.html", {"books": books})

def book_detail(request, isbn):
    book = get_object_or_404(Book.objects.select_related("author"), isbn=isbn)
    borrower = _borrower_for_user(request.user)
    open_loan = Loan.current_loan_for_book(book)

    if request.method == "POST":
        if borrower is None or not borrower.can_checkout(request.user):
            raise PermissionDenied()

        if open_loan is not None:
            return render(request, "book_detail.html", {
                "book": book,
                "borrower": borrower,
                "open_loan": open_loan,
                "error": "The book is already checked out",
            })

        now = timezone.now()
        Loan.objects.create(
            book=book,
            borrower=borrower,        
            borrower_name=borrower.name,     
            checked_out_at=now,
            due_at=now + timedelta(days=14),
            returned=False,
        )
        return redirect("book_detail", isbn=book.isbn)

    # GET
    return render(request, "book_detail.html", {
        "book": book,
        "borrower": borrower,
        "open_loan": open_loan,
        "error": None,
    })

@login_required
def librarian_dashboard(request):
    if not Librarian.is_librarian(request.user):
        raise PermissionDenied()

    if request.method == "POST":
        loan_id = request.POST.get("loan_id")
        loan = get_object_or_404(Loan, pk=loan_id)

        if not loan.can_mark_returned(request.user):
            raise PermissionDenied()

        loan.returned = True
        loan.save()
        return redirect("librarian")

    loans = Loan.objects.select_related("book").filter(returned=False).order_by("due_at")
    return render(request, "librarian.html", {"loans": loans})