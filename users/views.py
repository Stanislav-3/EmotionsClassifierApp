from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from .forms import RegisterForm, ProfileForm
from django.contrib.auth import get_user_model
from computations.models import Computation
import logging


logger = logging.getLogger(__name__)


class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profile')


class CustomPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('profile')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('login')


def home(request):
    logger.debug('Redirecting to /home')

    return render(request, 'users/home.html')


def sign_up(request):
    if request.method == 'POST':
        logger.debug('Sign up | POST')

        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('home'))
    else:
        logger.debug('Sign up | GET')
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {'form': form})


@login_required(login_url=reverse_lazy('login'))
def profile(request):
    links = None
    texts = None

    if request.method == 'POST':
        logger.debug('Profile view | POST')

        form = ProfileForm(request.POST, files=request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
    else:
        logger.debug('Profile view | GET')

        form = ProfileForm(instance=request.user)
        computations = Computation.objects.filter(user=request.user)

        links = [f'/computations/{request.user.username}/{computation.id}' for computation in computations]
        texts = [f'Computation #{computation.id}' for computation in computations]

    return render(request, 'users/profile.html', {'form': form, 'computations': zip(links, texts)})