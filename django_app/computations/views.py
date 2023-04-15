import io
import mimetypes

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from config.settings import BASE_DIR, DEBUG
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
from .image_preprocessing.transforms import images_to_base64, image_to_bytes
import requests

logger = logging.getLogger(__name__)


@login_required(login_url=reverse_lazy('login'))
def computations(request):
    if request.method == 'POST':
        logger.debug('rendering computations page | POST')

        in_memory_uploaded_file = request.FILES.get('image', None)

        # Check if image is not specified
        if in_memory_uploaded_file is None:
            return render(request, 'computations/computations.html', {
                'output': 'You didn\'t specify an image'
            })

        image = Image.open(in_memory_uploaded_file.file)
        if len(image.getbands()) == 4:
            image = image.convert('RGB')

        print("is_preprocessed: ", request.POST.get('is_preprocessed'))
        is_preprocessed = True if request.POST.get('is_preprocessed') == 'True' else False
        if not is_preprocessed:
            face_boxes = get_faces(image)
            if len(face_boxes) == 0:
                # No faces on the image
                return render(request, 'computations/computations.html', {
                    'output': 'We didn\'t find any face in your image :('
                })

            cropped_images = get_cropped_images(image, face_boxes)
            print(len(face_boxes))
            if len(face_boxes) > 1:
                # Multiple faces are on the image
                return render(request, 'computations/computations_choose_images.html', {
                    'images': images_to_base64(cropped_images),
                    'is_preprocessed': True
                })

            resized_image = get_resized_images(cropped_images)[0]
            cropped_image = cropped_images[0]
        else:
            resized_image = get_resized_images([image, ])[0]
            cropped_image = image

        flask_url = 'http://0.0.0.0:5001/get-emotions' if DEBUG else 'http://flask:5001/get-emotions'
        response = requests.post(flask_url, files={'image': image_to_bytes(resized_image)})
        probabilities = json.loads(response.text)

        # add a new computation to db
        file_content = ContentFile(image_to_bytes(cropped_image))
        computation = Computation(predictions=list(probabilities.values()),
                                  user=request.user)
        computation.save()
        computation.image.save(f'{computation.id}.jpg', file_content)

        return redirect(f'/computations/{computation.id}')
    elif request.method == 'GET':
        logger.debug('rendering computations page | GET')
        return render(request, 'computations/computations.html', {'output': 'Results will be there'})


@login_required(login_url=reverse_lazy('login'))
def computation_results(request, computation_id):
    logger.debug('rendering computations result page | GET')

    _computations = Computation.objects.filter(id=computation_id)
    if _computations.count() != 1 or _computations[0].user != request.user:
        return redirect(reverse('home'))

    return render(request, 'computations/result.html', {
        'predictions': _computations[0].predictions,
        'img_src': _computations[0].image.url
    })


target_names = {
    0: 'Angry',
    1: 'Disgust',
    2: 'Fear',
    3: 'Happy',
    4: 'Sad',
    5: 'Surprise',
    6: 'Neutral',
}


def _download(filebytes, filename, filetype):
    response = HttpResponse(filebytes, content_type=f'application/{filetype}')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


@login_required(login_url=reverse_lazy('login'))
def dump_json(request, computation_id):
    logger.debug(f'dump json')

    _computations = Computation.objects.filter(id=computation_id)
    if _computations.count() != 1 or _computations[0].user != request.user:
        return redirect(reverse('home'))

    with open(f'media/computations/images/{request.user.id}/{computation_id}.jpg', "rb") as image_file:
        filebytes = json.dumps({
            f'Computation': {
                'Predictions': _computations[0].predictions,
                'Image_format': 'jpeg',
                'Image_raw': str(image_file.read())
            }
        }).encode('utf-8')

    return _download(filebytes, 'Computations.json', 'json')


@login_required(login_url=reverse_lazy('login'))
def dump_pdf(request, computation_id):
    logger.debug(f'dump pdf')

    _computations = Computation.objects.filter(id=computation_id)
    if _computations.count() != 1 or _computations[0].user != request.user:
        return redirect(reverse('home'))
    predictions = _computations[0].predictions

    pdf = FPDF('P', 'mm', 'Letter')
    pdf.add_page()
    pdf.set_font('helvetica', 'b', 18)

    pdf.cell(0, 10, f'Image', ln=True)
    pdf.image(f'media/computations/images/{request.user.id}/{computation_id}.jpg', w=48, h=48)

    pdf.cell(0, 10, f'Predictions', ln=True)
    pdf.set_font('helvetica', '', 16)
    for i in range(len(predictions)):
        pdf.cell(0, 10, f'{target_names[i]}:{predictions[i]}', ln=True)

    filebytes = pdf.output(dest='s').encode('latin1')

    return _download(filebytes, 'Computations.pdf', 'pdf')
