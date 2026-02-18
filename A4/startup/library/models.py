from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=200)
    birth_year = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.birth_year})"

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=50, unique=True)
    published_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} ({self.isbn})"

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    borrower_name = models.CharField(max_length=200)
    checked_out_at = models.DateTimeField()
    due_at = models.DateTimeField()
    returned = models.BooleanField(default=False)

    def __str__(self):
        status = "returned" if self.returned else "out"
        return f"Loan({self.book.title} to {self.borrower_name}, {status})"