from itertools import chain

from django.contrib.auth.models import User
from django.db.models import CharField, Value, Q
from django.shortcuts import render, redirect

from litreview import settings
from litreview.models import Ticket, Review, UserFollows


def profile(request):
    if not request.user.is_authenticated:
        return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))

    tickets = Ticket.objects.filter(user=request.user).annotate(content_type=Value("TICKET", CharField()))
    reviews = Review.objects.filter(user=request.user).annotate(content_type=Value("REVIEW", CharField()))
    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)
    return render(request, "profile.html", {"posts": posts})


def home(request):
    users = User.objects.filter(
        followed_by__in=UserFollows.objects.filter(user=request.user).only("followed_user")
    ).only("id")

    tickets = Ticket.objects.filter(Q(user=request.user) | Q(user_id__in=users)).annotate(
        content_type=Value("TICKET", CharField())
    )

    reviews = Review.objects.filter(
        Q(user=request.user) | Q(user_id__in=users) | Q(ticket__in=Ticket.objects.filter(user=request.user))
    ).annotate(content_type=Value("REVIEW", CharField()))

    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    return render(request, "home.html", {"posts": posts})
