from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

from litreview.forms.ticket_form import TicketForm
from litreview.models import Ticket


def create(request):
    if not request.user.is_authenticated:
        return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = Ticket.objects.create(user=request.user)
            form.handle(ticket)
            return redirect("home")
    else:
        form = TicketForm()
    return render(request, "tickets/create.html", {"form": form})


def read(request, id: int):
    pass


def update(request, id: int):
    if not request.user.is_authenticated:
        return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))

    ticket = Ticket.objects.get(id=id)

    if request.user != ticket.user:
        raise PermissionDenied()

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.handle(ticket)
            return redirect("home")
    else:
        form = TicketForm({"title": ticket.title, "description": ticket.description})
    return render(request, "tickets/update.html", {"form": form, "ticket": ticket})


def delete(request, id: int):
    if not request.user.is_authenticated:
        return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))

    ticket = Ticket.objects.get(id=id)

    if request.user != ticket.user:
        raise PermissionDenied()

    ticket.delete()
    return redirect("home")
