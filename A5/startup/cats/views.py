from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse
from .models import Owner, Cat
# Create your views here.

def index(request):
    return HttpResponse("<h1>Welcome to the Cat Tracker!</h1>")

def author(request):
    return HttpResponse("<h1>By David Johnson!</h1>")

def detail(request, owner_id):
    output = ""
    output += "<h1>Owner</h1>"
    owner = Owner.objects.get(id=owner_id)
    output += str(owner)
    output += "<h1>Cats</h1>"
    cats = owner.cat_set.all()
    output += "<ul>"
    for cat in cats:
        output += "<li>" + str(cat) + "</li>"
    output += "</ul>"

    return HttpResponse(output)