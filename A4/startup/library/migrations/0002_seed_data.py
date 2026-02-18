from django.db import migrations
from django.utils import timezone
from django.utils.dateparse import parse_datetime

def forwards(apps, schema_editor):
    Author = apps.get_model("library", "Author")
    Book = apps.get_model("library", "Book")
    Loan = apps.get_model("library", "Loan")

    a, _ = Author.objects.get_or_create(name="Jane Doe", defaults={"birth_year": 1980})

    b1, _ = Book.objects.get_or_create(
        isbn="ISBN-ALPHA-001",
        defaults={"author": a, "title": "Alpha", "published_year": 2010},
    )
    b2, _ = Book.objects.get_or_create(
        isbn="ISBN-BETA-002",
        defaults={"author": a, "title": "Beta", "published_year": 2012},
    )

    Loan.objects.get_or_create(
        book=b1,
        borrower_name="Nick",
        checked_out_at=timezone.make_aware(parse_datetime("2026-02-04 10:00")),
        due_at=timezone.make_aware(parse_datetime("2026-02-18 10:00")),
        defaults={"returned": True},
    )
    Loan.objects.get_or_create(
        book=b2,
        borrower_name="Sam",
        checked_out_at=timezone.make_aware(parse_datetime("2026-02-04 11:00")),
        due_at=timezone.make_aware(parse_datetime("2026-02-18 11:00")),
        defaults={"returned": False},
    )

def backwards(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [("library", "0001_initial")]
    operations = [migrations.RunPython(forwards, backwards)]