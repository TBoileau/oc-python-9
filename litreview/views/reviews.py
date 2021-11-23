from django.core.exceptions import BadRequest
from django.shortcuts import redirect, render

from litreview import settings
from litreview.forms.review_form import ReviewForm
from litreview.models import Review, Ticket


def create(request, ticket_id: int):
    if not request.user.is_authenticated:
        return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))

    ticket = Ticket.objects.get(id=ticket_id)

    if Review.objects.filter(ticket=ticket).exists():
        raise BadRequest()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = Review(user=request.user, ticket=ticket)
            form.handle(review)
            return redirect("home")
    else:
        form = ReviewForm()
    return render(request, "reviews/create.html", {"form": form, "ticket": ticket})
