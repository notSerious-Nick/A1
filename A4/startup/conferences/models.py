from django.db import models

class Venue(models.Model):
    name = models.CharField(max_length=200)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.name} (cap {self.capacity})"

class Event(models.Model):
    venue = models.ForeignKey(Venue, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    starts_at = models.DateTimeField()
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        status = "cancelled" if self.is_cancelled else "active"
        return f"{self.title} ({status})"

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee_email = models.EmailField()
    registered_at = models.DateTimeField()
    checked_in = models.BooleanField(default=False)

    def __str__(self):
        return f"Reg({self.attendee_email} -> {self.event.title})"