from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from src.forms.login_form import LoginForm


def home(request):
    return render(request, 'home.html', {})

def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
