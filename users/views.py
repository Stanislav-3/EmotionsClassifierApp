from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


def home(request):
    return render(request, 'users/home.html')


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('home'))
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {'form': form})


@login_required(login_url=reverse_lazy('login'))
def profile(request):
    return render(request, 'users/profile.html')