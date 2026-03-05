from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=200)
    birth_year = models.IntegerField()

    def __str__(self):
        return f"Author(name={self.name}, birth_year={self.birth_year})"


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=32, unique=True)
    published_year = models.IntegerField()

    def __str__(self):
        return f"Book(title={self.title}, isbn={self.isbn}, year={self.published_year}, author={self.author.name})"


# new for A6

class Borrower(models.Model):
    name = models.CharField(max_length=200)

    # optional link to Django user
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="borrower",
    )

    def __str__(self):
        return f"Borrower(name={self.name})"

    def can_checkout(self, user) -> bool:
        # user must exist + authenticated
        if user is None or not user.is_authenticated:
            return False
        # must be linked to this borrower
        if self.account_id != user.id:
            return False
        # borrower must have < 2 active loans
        return self.loans.filter(returned=False).count() < 2


class Librarian(models.Model):
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,   # deleted when User is deleted
        related_name="librarian",
    )

    def __str__(self):
        return f"Librarian(account={self.account.username})"

    @classmethod
    def is_librarian(cls, user) -> bool:
        return user is not None and user.is_authenticated and cls.objects.filter(account=user).exists()

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    borrower_name = models.CharField(max_length=200)

    borrower = models.ForeignKey(
        Borrower,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="loans",
    )

    checked_out_at = models.DateTimeField()
    due_at = models.DateTimeField()
    returned = models.BooleanField(default=False)

    @classmethod
    def current_loan_for_book(cls, book):
        return cls.objects.filter(book=book, returned=False).first()

    def can_mark_returned(self, user) -> bool:
        return Librarian.is_librarian(user)