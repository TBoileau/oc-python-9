from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm your password', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            self.add_error('username', f"{username} is taken.")

        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email', f"{email} is taken.")

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if confirm_password != password:
            self.add_error('confirm_password', f"{confirm_password} does not match with your password.")

        return self.cleaned_data


    def handle(self):
        user = User.objects.create_user(
            username=self.cleaned_data.get("username"),
            email=self.cleaned_data.get("email"),
            password=self.cleaned_data.get("password")
        )
        user.save()
