from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import ComputationForm


def computations(request):
    if request.method == 'POST':
        form = ComputationForm(request.POST)
        if form.is_valid():
            # compute
            form.save()
            # print result
            # return redirect(reverse('home'))
    else:
        form = ComputationForm()

    return render(request, 'computations/computations.html', {'form': form})
