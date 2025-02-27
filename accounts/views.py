from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import ManagerRegistrationForm
from django.contrib.auth.models import Group

def register(request):
    if request.method == "POST":
        form = ManagerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            managers_group, created = Group.objects.get_or_create(name="Managers")
            user.groups.add(managers_group)
            login(request, user)
            return redirect("home")
    else:
        form = ManagerRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})

@login_required
def home(request):
    return render(request, "index.html")

def redirect_unknown(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('login')