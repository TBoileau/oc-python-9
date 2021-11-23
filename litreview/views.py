from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from litreview.forms.sign_in_form import SignInForm
from litreview.forms.sign_up_form import SignUpForm
from litreview.models import UserFollows


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


def subscriptions(request):
    if not request.user.is_authenticated:
        return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))

    subscriptions = UserFollows.objects.filter(user=request.user)
    subscribers = UserFollows.objects.filter(followed_user=request.user)

    return render(request, "subscriptions.html", {"subscriptions": subscriptions, "subscribers": subscribers})


def unsubscribe(request, followed_user: int):
    if not request.user.is_authenticated:
        return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))

    user_follow = UserFollows.objects.get(user=request.user, followed_user_id=followed_user)
    user_follow.delete()
    return redirect("/subscriptions")
