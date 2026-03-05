from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=200)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Venue(name={self.name}, capacity={self.capacity})"


class Event(models.Model):
    # Allow event to survive if venue is deleted:
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    starts_at = models.DateTimeField()
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        venue_part = self.venue.name if self.venue else "None"
        return f"Event(title={self.title}, starts_at={self.starts_at}, venue={venue_part}, cancelled={self.is_cancelled})"


class Registration(models.Model):
    # Appropriate: if an event is deleted, registrations should not remain behind
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee_email = models.EmailField()
    registered_at = models.DateTimeField()
    checked_in = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"Registration(event={self.event.title}, email={self.attendee_email}, "
            f"registered_at={self.registered_at}, checked_in={self.checked_in})"
        )
