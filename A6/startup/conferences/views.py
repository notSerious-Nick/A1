from django.shortcuts import render

# Create your views here.
from datetime import datetime

from django.shortcuts import render
from django.utils import timezone

from .models import Event, Registration


from django.shortcuts import render
from django.utils import timezone

from .models import Event, Registration


def registration_form(request):
    """
    Manual HTML form (no Django Forms).
    Collect validation errors and re-render the form with a list of messages.
    """
    errors = []

    # For repopulating the form when re-rendering
    values = {
        "event_id": "",
        "attendee_email": "",
        "checked_in": False,
    }

    if request.method == "POST":
        # Read inputs
        event_id_raw = (request.POST.get("event_id") or "").strip()
        attendee_email = (request.POST.get("attendee_email") or "").strip()
        checked_in = ("checked_in" in request.POST)

        # Save values for redisplay
        values["event_id"] = event_id_raw
        values["attendee_email"] = attendee_email
        values["checked_in"] = checked_in

        # --- Validate event_id ---
        event = None
        try:
            event_id = int(event_id_raw)
            if event_id < 1:
                errors.append("Event ID must be at least 1.")
            else:
                event = Event.objects.filter(id=event_id).first()
                if event is None:
                    errors.append("No event exists with that Event ID.")
        except ValueError:
            errors.append("Event ID must be a whole number.")

        # --- Validate attendee_email (simple check allowed) ---
        if attendee_email == "":
            errors.append("Email is required.")
        else:
            # Very simple email-ish check (course-appropriate)
            if "@" not in attendee_email or "." not in attendee_email:
                errors.append("Please enter a valid email address.")

        # --- Business rule: cancelled events cannot be registered ---
        if event is not None and event.is_cancelled:
            errors.append("This event is cancelled, so registrations are not allowed.")

        # If any errors, re-render form once
        if errors:
            return render(
                request,
                "conferences/registration_form.html",
                {"errors": errors, "values": values},
            )

        # Success: create registration
        reg = Registration.objects.create(
            event=event,
            attendee_email=attendee_email,
            registered_at=timezone.now(),
            checked_in=checked_in,
        )

        return render(
            request,
            "conferences/registration_confirmation.html",
            {"registration": reg, "event": event},
        )

    # GET: show empty form
    return render(
        request,
        "conferences/registration_form.html",
        {"errors": [], "values": values},
    )


def event_list(request):
    """
    A5 Part 2B: Template-based event list + GET filter checkbox show_cancelled.
    """
    qs = Event.objects.all().order_by("starts_at")

    show_cancelled = bool(request.GET.get("show_cancelled"))
    if not show_cancelled:
        qs = qs.filter(is_cancelled=False)

    return render(
        request,
        "conferences/event_list.html",
        {
            "events": qs,
            "show_cancelled": show_cancelled,  # optional; template can also read request.GET
        },
    )
