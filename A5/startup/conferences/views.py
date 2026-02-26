from django.shortcuts import render

# Create your views here.
from datetime import datetime

from django.shortcuts import render
from django.utils import timezone

from .models import Event, Registration
def event_list(request):
    show_cancelled = "show_cancelled" in request.GET

    qs = Event.objects.order_by("starts_at")
    if not show_cancelled:
        qs = qs.filter(is_cancelled=False)

    return render(request, "conferences/event_list.html", {
        "events": qs,
        "show_cancelled": show_cancelled,
    })

def registration_form(request):
    """
    A5 Part 2B:
    Collect validation errors and re-render the form
    with a list of error messages.
    """
    context = {
        "errors": [],
        "event_id": "",
        "attendee_email": "",
        "checked_in": False,
    }

    if request.method == "GET":
        return render(request, "conferences/registration_form.html", context)

    # POST
    event_id_raw = request.POST.get("event_id", "").strip()
    email = request.POST.get("attendee_email", "").strip()
    checked_in = request.POST.get("checked_in") == "on"

    # keep submitted values
    context["event_id"] = event_id_raw
    context["attendee_email"] = email
    context["checked_in"] = checked_in

    # validate event_id (int + exists)
    event = None
    try:
        event_id = int(event_id_raw)
        if event_id < 1:
            context["errors"].append("event_id must be at least 1.")
        else:
            event = Event.objects.filter(id=event_id).first()
            if event is None:
                context["errors"].append("event_id must refer to an existing Event.")
    except ValueError:
        context["errors"].append("event_id must be an integer.")

    # validate email (simple)
    if not email:
        context["errors"].append("attendee_email is required.")
    else:
        if ("@" not in email) or ("." not in email):
            context["errors"].append("attendee_email must look like a valid email address.")

    # reject cancelled event
    if event is not None and event.is_cancelled:
        context["errors"].append("Cannot register for a cancelled event.")

    # if errors, show form again
    if context["errors"]:
        return render(request, "conferences/registration_form.html", context)

    # create Registration
    reg = Registration.objects.create(
        event=event,
        attendee_email=email,
        checked_in=checked_in,
        registered_at=timezone.now(),
    )

    return render(
        request,
        "conferences/registration_confirmation.html",
        {"registration": reg},
    )
