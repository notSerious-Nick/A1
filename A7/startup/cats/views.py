from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse
from .models import Cat, Owner
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def index(request):
    output = "<h1>Welcome to the Cat Tracker!</h1>"
    output += "<h2>Cats</h2>"
    cats = Cat.objects.all()
    output += "<ul>"
    for cat in cats:
        output += "<li>" + cat.name + "</li>"
    output += "</ul>"

    return HttpResponse(output)


def owner(request, owner_id):
    me = get_object_or_404(Owner,id=owner_id)
    cats = me.cat_set.all()

    context = {"owner": me, "cats": cats}
    return render(request, "owner.html", context)


def login_user(request):
    if request.method == "POST":
       username = request.POST.get("username")
       password = request.POST.get("password")

       user = authenticate(request, username=username, password=password)
       if user is not None:
           login(request, user)
           return redirect(f"/cats/")
       else:
           return render(request, "login.html", {"error":"Invalid"})

    return render(request, "login.html")

@login_required
def logout_owner(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/cats/') # 'home' is a named URL pattern
    return redirect('/cats/')

@login_required
def add_cat(request):
    errors = {}
    print(request.user)
    if request.method == "POST":
        cat_name = request.POST["catname"]
        cat_age = request.POST["catage"]
        cat_owner = request.POST["catowner"]
        cat_owner_object = Owner.objects.get(name=cat_owner)
        new_cat = Cat(name=cat_name, age=cat_age, owner=cat_owner_object)
        new_cat.save()
        # go somewhere else
        return redirect(f"/cats/Owner/{cat_owner_object.id}")
    return render(request, "add-cat.html", {"errors": errors})

@login_required
def edit_cat(request, cat_id):
    cat = get_object_or_404(Cat, pk=cat_id)

    if not cat.can_edit(request.user):
        raise PermissionDenied("Not the owner")

    if request.method == "POST":
        name = request.POST.get("name", "")
        age = request.POST.get("age", "")

        if not name or not age.isdigit():
            return render(request, "edit_cat.html",
                        {"cat": cat, "error": "Bad entry"})
        
        cat.name = name
        cat.age = int(age)
        cat.save()
        return redirect("index")
    
    return render(request, "edit_cat.html",
                    {"cat": cat})


