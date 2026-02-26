from django.http import HttpResponse
from django.utils.dateparse import parse_datetime

from .models import Author, Book, Loan


def q1_all_authors(request):
    qs = Author.objects.order_by("name")
    output = "<ul>"
    for a in qs:
        output += f"<li>{a}</li>"
    output += "</ul>"
    return HttpResponse(output)


def q2_all_books(request):
    qs = Book.objects.order_by("-published_year")
    output = "<ul>"
    for b in qs:
        output += f"<li>{b}</li>"
    output += "</ul>"
    return HttpResponse(output)


def q3_books_after_year(request, year):
    qs = Book.objects.filter(published_year__gt=year).order_by("published_year")
    output = "<ul>"
    for b in qs:
        output += f"<li>{b} ({b.published_year})</li>"
    output += "</ul>"
    return HttpResponse(output)


def q4_books_by_author(request, author_id):
    qs = Book.objects.filter(author__id=author_id).order_by("published_year")
    output = "<ul>"
    for b in qs:
        output += f"<li>{b}</li>"
    output += "</ul>"
    return HttpResponse(output)


def q5_open_loans(request):
    qs = Loan.objects.filter(returned=False)
    output = "<ul>"
    for loan in qs:
        # assuming Loan has borrower_name and book FK; display borrower + book title
        output += f"<li>{loan.borrower_name} — {loan.book.title}</li>"
    output += "</ul>"
    return HttpResponse(output)


def q6_loans_due_before(request):
    t_str = request.GET.get("t")
    if not t_str:
        return HttpResponse("<p>Error: missing time parameter 't'.</p>")

    t = parse_datetime(t_str)
    if t is None:
        return HttpResponse("<p>Error: invalid time format. Use YYYY-MM-DD HH:MM</p>")

    qs = Loan.objects.filter(due_at__lt=t).order_by("due_at")
    output = "<ul>"
    for loan in qs:
        output += f"<li>{loan.borrower_name} — {loan.book.title} (due {loan.due_at})</li>"
    output += "</ul>"
    return HttpResponse(output)


def q7_book_by_isbn(request, isbn):
    book = Book.objects.filter(isbn=isbn).first()
    if book is None:
        return HttpResponse("<p>No matching book found.</p>")
    return HttpResponse(f"<p>{book}</p>")


def q8_stats(request):
    num_authors = Author.objects.count()
    num_books = Book.objects.count()
    num_loans = Loan.objects.count()
    num_open_loans = Loan.objects.filter(returned=False).count()

    output = "<ul>"
    output += f"<li>Authors: {num_authors}</li>"
    output += f"<li>Books: {num_books}</li>"
    output += f"<li>Loans: {num_loans}</li>"
    output += f"<li>Open loans: {num_open_loans}</li>"
    output += "</ul>"
    return HttpResponse(output)