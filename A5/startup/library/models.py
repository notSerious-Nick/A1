from django.db import models


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


class Loan(models.Model):
    # Sensible choice: if a book is removed, its loans disappear as well
    # (alternative would be PROTECT, but CASCADE is a clean default for the course)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    borrower_name = models.CharField(max_length=200)
    checked_out_at = models.DateTimeField()
    due_at = models.DateTimeField()
    returned = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"Loan(book={self.book.title}, borrower={self.borrower_name}, "
            f"out={self.checked_out_at}, due={self.due_at}, returned={self.returned})"
        )
