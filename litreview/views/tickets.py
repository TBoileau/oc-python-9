from django.conf import settings
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
    pass


def delete(request, id: int):
    pass
