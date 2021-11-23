from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from litreview.forms.sign_in_form import SignInForm
from litreview.forms.sign_up_form import SignUpForm


def home(request):
    return render(request, "home.html", {})


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.handle()
            return redirect("sign_in")
    else:
        form = SignUpForm()
    return render(request, "sign_up.html", {"form": form})


def sign_in(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            username, password = form.cleaned_data.values()
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")
    else:
        form = SignInForm()
    return render(request, "sign_in.html", {"form": form})
