from django import forms

from litreview.models import Review


class ReviewWithoutTicketForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description", required=False, widget=forms.Textarea)
    image = forms.ImageField(label="Image", required=False)
    headline = forms.CharField(label="Headline", required=False)
    body = forms.CharField(label="Body", required=False, widget=forms.Textarea)
    rating = forms.TypedChoiceField(
        label="Rating",
        coerce=int,
        widget=forms.RadioSelect,
        choices=[
            (0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
        ],
    )

    def handle(self, review: Review):
        review.ticket.title = self.cleaned_data.get("title")
        review.ticket.description = self.cleaned_data.get("description")
        review.ticket.image = self.cleaned_data.get("image")
        review.ticket.save()

        review.headline = self.cleaned_data.get("headline")
        review.rating = int(self.cleaned_data.get("rating"))
        review.body = self.cleaned_data.get("body")
        review.save()
