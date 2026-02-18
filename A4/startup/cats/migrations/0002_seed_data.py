from django.db import migrations
from django.utils import timezone
from django.utils.dateparse import parse_datetime

def forwards(apps, schema_editor):
    Owner = apps.get_model("cats", "Owner")
    Cat = apps.get_model("cats", "Cat")
    VetVisit = apps.get_model("cats", "VetVisit")

    o, _ = Owner.objects.get_or_create(name="Clinic Owner")

    tulip, _ = Cat.objects.get_or_create(name="Tulip", defaults={"age": 2, "owner": o})
    geyser, _ = Cat.objects.get_or_create(name="Geyser", defaults={"age": 4, "owner": o})

    VetVisit.objects.get_or_create(
        cat=tulip,
        visit_time=timezone.make_aware(parse_datetime("2026-02-04 14:30")),
        defaults={"reason": "Checkup", "weight_lbs": 12.3, "paid": False, "cost_usd": 55.00},
    )
    VetVisit.objects.get_or_create(
        cat=geyser,
        visit_time=timezone.make_aware(parse_datetime("2026-02-05 09:15")),
        defaults={"reason": "Vaccines", "weight_lbs": 10.8, "paid": True, "cost_usd": 75.50},
    )

def backwards(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [("cats", "0001_initial")]
    operations = [migrations.RunPython(forwards, backwards)]