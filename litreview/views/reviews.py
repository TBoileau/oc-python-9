from django.core.exceptions import BadRequest
from django.shortcuts import redirect, render

from litreview import settings
from litreview.forms.review_form import ReviewForm
from litreview.forms.review_without_ticket_form import ReviewWithoutTicketForm
from litreview.models import Review, Ticket


def create(request, ticket_id: int = None):
    if not request.user.is_authenticated:
        return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))

    if ticket_id is not None:
        ticket = Ticket.objects.get(id=ticket_id)

        if Review.objects.filter(ticket=ticket).exists():
            raise BadRequest()
    else:
        ticket = Ticket(user=request.user)

    if request.method == "POST":
        form = (
            ReviewForm(request.POST) if ticket_id is not None else ReviewWithoutTicketForm(request.POST, request.FILES)
        )
        if form.is_valid():
            review = Review(user=request.user, ticket=ticket)
            form.handle(review)
            return redirect("home")
    else:
        form = (
            ReviewForm(request.POST) if ticket_id is not None else ReviewWithoutTicketForm(request.POST, request.FILES)
        )
    return render(request, "reviews/create.html", {"form": form, "ticket": ticket})
