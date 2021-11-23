from django import forms
from django.contrib.auth.models import User

from litreview.models import UserFollows


class SubscribeForm(forms.Form):
    username = forms.CharField(label="Username")

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        if not User.objects.filter(username=username).exists():
            self.add_error("username", f"{username} does not exist.")
        else:
            followed_user = User.objects.get(username=username)

            if UserFollows.objects.filter(followed_user=followed_user).exists():
                self.add_error("username", f"You already follow {username}.")

        return self.cleaned_data

    def handle(self, user: User):
        UserFollows.objects.create(
            user=user, followed_user=User.objects.get(username=self.cleaned_data.get("username"))
        )
