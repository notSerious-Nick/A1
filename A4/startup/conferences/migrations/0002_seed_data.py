from django.db import migrations
from django.utils import timezone
from django.utils.dateparse import parse_datetime

def forwards(apps, schema_editor):
    Venue = apps.get_model("conferences", "Venue")
    Event = apps.get_model("conferences", "Event")
    Registration = apps.get_model("conferences", "Registration")

    v, _ = Venue.objects.get_or_create(name="Main Hall", defaults={"capacity": 300})

    e1, _ = Event.objects.get_or_create(
        title="Tech Talk",
        starts_at=timezone.make_aware(parse_datetime("2026-02-10 18:00")),
        defaults={"venue": v, "is_cancelled": False},
    )
    e2, _ = Event.objects.get_or_create(
        title="Cancelled Meetup",
        starts_at=timezone.make_aware(parse_datetime("2026-02-11 18:00")),
        defaults={"venue": v, "is_cancelled": True},
    )

    Registration.objects.get_or_create(
        event=e1,
        attendee_email="a@example.com",
        registered_at=timezone.make_aware(parse_datetime("2026-02-04 09:00")),
        defaults={"checked_in": False},
    )
    Registration.objects.get_or_create(
        event=e1,
        attendee_email="b@example.com",
        registered_at=timezone.make_aware(parse_datetime("2026-02-04 09:05")),
        defaults={"checked_in": True},
    )
    Registration.objects.get_or_create(
        event=e2,
        attendee_email="c@example.com",
        registered_at=timezone.make_aware(parse_datetime("2026-02-04 09:10")),
        defaults={"checked_in": False},
    )

def backwards(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [("conferences", "0001_initial")]
    operations = [migrations.RunPython(forwards, backwards)]