import torch
from torch import nn
import json
from torchvision import transforms
from PIL import Image
from model import Net
import numpy as np
from multiprocessing import Process, Queue

target_names = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

model, mean_var = None, {}
model_queue, mean_var_queue = Queue(), Queue()


def apply_transformations(image, mean_var):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda image: image.repeat(3, 1, 1)),
        transforms.Normalize(mean_var['mean'], mean_var['var'])
    ])

    return transform(image)


def load_model(queue: Queue):
    model = Net()
    model.load_state_dict(torch.load('weights/model.pth', map_location=torch.device('cpu')))
    model.eval()

    queue.put(model)


def load_mean_var(queue: Queue):
    with open('weights/mean_var.json') as file:
        mean_var = json.load(file)
        queue.put(mean_var)


def load_evaluation_stuff():
    global model, mean_var

    load_model_process = Process(target=load_model, args=(model_queue,))
    load_model_process.start()
    load_mean_var_precess = Process(target=load_mean_var, args=(mean_var_queue,))
    load_mean_var_precess.start()

    load_mean_var_precess.join()
    mean_var = mean_var_queue.get()

    load_model_process.join()
    model = model_queue.get()


@torch.no_grad()
def evaluate(image: Image):
    if image.mode != 'L':
        image = image.convert('L')

    if model is None or mean_var == {}:
        raise ValueError('Model is not yet configured')

    transformed = apply_transformations(image, mean_var)
    outputs = model(transformed.unsqueeze(0))

    probabilities = nn.Softmax(dim=0)(outputs[0])
    probabilities = map(str, probabilities.numpy())

    return dict(zip(target_names, probabilities))
