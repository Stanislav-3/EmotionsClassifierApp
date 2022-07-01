from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Computation
from computations.evaluation import predict
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
import numpy as np


target_names = {
    0: 'Angry',
    1: 'Disgust',
    2: 'Fear',
    3: 'Happy',
    4: 'Sad',
    5: 'Surprise',
    6: 'Neutral',
}


def beautify_probabilities(probabilities):
    output = '\n'
    for idx in np.argsort(probabilities)[::-1]:
        tabs = '\t\t' if len(target_names[idx]) > 3 else '\t\t\t'
        output += f'{target_names[idx]} {tabs} {100 * probabilities[idx]:.1f}\n'

    return output


def computations(request):
    if request.method == 'POST':
        image = request.FILES['image'].file
        # output = request.POST['output']
        probabilities = predict(image)

        output = beautify_probabilities(probabilities)

        # add a new computation to db
        file_content = ContentFile(request.FILES['image'].read())
        computation = Computation(predictions=list(probabilities),
                                  user=request.user)
        computation.save()
        computation.image.save(f'{computation.id}.jpg', file_content)

        return redirect(f'/computations/{request.user.username}/{computation.id}')
    else:
        return render(request, 'computations/computations.html', {'output': 'Results will be here'})


def result(request, username, computation_id):
    computation = Computation.objects.filter(id=computation_id)
    user = get_user_model().objects.filter(username=username)

    if computation.count() != 1 or user.count() != 1:
        return redirect(reverse('home'))

    computation, user = computation[0], user[0]
    if computation.user != user:
        return redirect(reverse('home'))

    return render(request, 'computations/result.html', {
        'predictions': beautify_probabilities(computation.predictions),
        'img_src': computation.image.url
    })
