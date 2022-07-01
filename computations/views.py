from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import ComputationForm
from .models import Computation
from computations.evaluation import predict
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


target_names = {
    0: 'Angry',
    1: 'Disgust',
    2: 'Fear',
    3: 'Happy',
    4: 'Sad',
    5: 'Surprise',
    6: 'Neutral',
}


def computations(request):
    output = 'Results will be here'

    if request.method == 'POST':
        image = request.FILES['image'].file
        # output = request.POST['output']
        probabilities = predict(image)
        output = '\n'
        for idx in probabilities.argsort()[::-1]:
            tabs = '\t\t' if len(target_names[idx]) > 3 else '\t\t\t'
            output += f'{target_names[idx]} {tabs} {100 * probabilities[idx]:.1f}\n'

        # add a new computation to db
        file_content = ContentFile(request.FILES['image'].read())
        computation = Computation(predictions=list(probabilities),
                                  user=request.user)
        computation.save()
        computation.image.save(f'{computation.id}.jpg', file_content)
    else:
        pass

    return render(request, 'computations/computations.html', {'output': output})
