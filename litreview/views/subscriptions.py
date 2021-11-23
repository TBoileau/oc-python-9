from django.conf import settings
from django.shortcuts import redirect, render

from litreview.forms.subscribe_form import SubscribeForm
from litreview.models import UserFollows


def subscriptions(request):
    if not request.user.is_authenticated:
        return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))

    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.handle(request.user)
            return redirect("subscriptions")
    else:
        form = SubscribeForm()

    subscriptions = UserFollows.objects.filter(user=request.user)
    subscribers = UserFollows.objects.filter(followed_user=request.user)

    return render(
        request, "subscriptions.html", {"form": form, "subscriptions": subscriptions, "subscribers": subscribers}
    )


def unsubscribe(request, followed_user: int):
    if not request.user.is_authenticated:
        return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))

    user_follow = UserFollows.objects.get(user=request.user, followed_user_id=followed_user)
    user_follow.delete()
    return redirect("/subscriptions")
