import mimetypes

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django_app.settings import BASE_DIR
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model

from .models import Computation
import json
import os
from fpdf import FPDF
import logging
import numpy as np
from PIL import Image
from .image_preprocessing.face_detection import get_faces
from .image_preprocessing.image_crop import get_cropped_images, get_resized_images

logger = logging.getLogger(__name__)


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
    logger.debug('computations.models get upload path')

    output = '\n'
    for idx in np.argsort(probabilities)[::-1]:
        tabs = '\t\t' if len(target_names[idx]) > 3 else '\t\t\t'
        output += f'{target_names[idx]} {tabs} {100 * probabilities[idx]:.1f}\n'

    return output


@login_required(login_url=reverse_lazy('login'))
def computations(request):
    if request.method == 'POST':
        logger.debug('rendering computations page | POST')

        image = Image.open(request.FILES['image'].file)

        image, face_boxes = get_faces(image)
        cropped_images = get_cropped_images(image, face_boxes)
        resized_images = get_resized_images(cropped_images)

        probabilities = [0.1428571429] * 7

        output = beautify_probabilities(probabilities)

        # add a new computation to db
        file_content = ContentFile(request.FILES['image'].read())
        computation = Computation(predictions=list(probabilities),
                                  user=request.user)
        computation.save()
        computation.image.save(f'{computation.id}.jpg', file_content)

        return redirect(f'/computations/{request.user.username}/{computation.id}')
    else:
        logger.debug('rendering computations page | GET')
        return render(request, 'computations/computations.html', {'output': 'Results will be here'})


@login_required(login_url=reverse_lazy('login'))
def result(request, username, computation_id):
    logger.debug('rendering computations result page | GET')

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


@login_required(login_url=reverse_lazy('login'))
def _download(request, username, computation_id, ext):
    logger.debug(f'_download {request.user.username}/{computation_id}.{ext}')

    filename = f'{computation_id}.{ext}'
    filepath = f'{BASE_DIR}/computations/dumps/{ext}/{request.user.username}/{filename}'

    file = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(file, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


@login_required(login_url=reverse_lazy('login'))
def dump_json(request, username, computation_id):
    logger.debug(f'dump json')

    directory = f'computations/dumps/json/{request.user.username}'
    computation = Computation.objects.filter(id=computation_id)[0]

    if os.path.exists(directory):
        if os.path.exists(f'{directory}/{computation_id}.json'):
            return _download(request, username, computation_id, 'json')
    else:
        os.makedirs(directory)

    b = None

    with open(f'media/computations/images/{request.user.id}/{computation_id}.jpg', "rb") as image:
        b = str(image.read())

    d = {f'Computation': {
        'Image': b,
        'Predictions': computation.predictions

    }}

    f = open(f'{directory}/{computation.id}.json', 'w')
    json.dump(d, f)

    return _download(request, username, computation_id, 'json')


@login_required(login_url=reverse_lazy('login'))
def dump_pdf(request, username, computation_id):
    logger.debug(f'dump pdf')

    directory = f'computations/dumps/pdf/{request.user.username}'

    if os.path.exists(directory):
        if os.path.exists(f'{directory}/{computation_id}.pdf'):
            return _download(request, username, computation_id, 'pdf')
    else:
        os.makedirs(directory)

    pdf = FPDF('P', 'mm', 'Letter')

    pdf.add_page()

    computation = Computation.objects.filter(id=computation_id)[0]
    predictions = computation.predictions

    pdf.set_font('helvetica', 'b', 18)
    pdf.cell(0, 10, f'Image', ln=True)
    pdf.image(f'media/computations/images/{request.user.id}/{computation_id}.jpg', w=48, h=48)

    pdf.cell(0, 10, f'Predictions', ln=True)
    pdf.set_font('helvetica', '', 16)
    for i in range(len(predictions)):
        pdf.cell(0, 10, f'{target_names[i]}:{predictions[i]}', ln=True)

    pdf.output(f'{directory}/{computation_id}.pdf')

    return _download(request, username, computation_id, 'pdf')