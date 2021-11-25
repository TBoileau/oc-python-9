from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from litreview.forms.sign_in_form import SignInForm
from litreview.forms.sign_up_form import SignUpForm


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.handle()
            return redirect("sign_in")
    else:
        form = SignUpForm()
    return render(request, "security/sign_up.html", {"form": form})


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
    return render(request, "security/sign_in.html", {"form": form})
