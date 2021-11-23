from django import forms

from litreview.models import Ticket


class TicketForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description", required=False, widget=forms.Textarea)
    image = forms.ImageField(label="Image", required=False)

    def handle(self, ticket: Ticket):
        ticket.title = self.cleaned_data.get("title")
        ticket.description = self.cleaned_data.get("description")
        ticket.image = self.cleaned_data.get("image")
        ticket.save()
