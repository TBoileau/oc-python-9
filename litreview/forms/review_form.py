from django import forms

from litreview.models import Review


class ReviewForm(forms.Form):
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
        review.headline = self.cleaned_data.get("headline")
        review.rating = int(self.cleaned_data.get("rating"))
        review.body = self.cleaned_data.get("body")
        review.save()
