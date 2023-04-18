import torch
from torch import nn
import json
from torchvision import transforms
from PIL import Image
from model import Net
import numpy as np
# from multiprocessing import Process, Queue
import torch.multiprocessing as mp
mp.set_start_method('fork')


target_names = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

model, mean_std = None, {}
model_queue, mean_std_queue = mp.Queue(), mp.Queue()
# load_mean_std_precess, load_model_process = None, None

was_in_loading = False


def apply_transformations(image, mean_std):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda image: image * 255),
        transforms.Lambda(lambda image: image.repeat(3, 1, 1)),
        transforms.Normalize(mean_std['mean'], mean_std['std'])
    ])

    return transform(image)


def load_model(queue: mp.Queue or None):
    model = Net()
    model.load_state_dict(torch.load('weights/model.pth', map_location=torch.device('cpu')))
    model.eval()

    if queue:
        queue.put(model)
    else:
        return model


def load_mean_std(queue: mp.Queue or None):
    with open('weights/mean_std.json') as file:
        mean_std = json.load(file)

        if queue:
            queue.put(mean_std)
        else:
            return mean_std


# def load_evaluation_stuff():
#     global load_model_process, load_mean_std_precess, model, mean_std
#     print('Started to load')
#
#     if model is not None and mean_std != {}:
#         return
#
#     load_model_process = mp.Process(target=load_model, args=(model_queue,))
#     load_model_process.start()
#     load_mean_std_precess = mp.Process(target=load_mean_std, args=(mean_std_queue,))
#     load_mean_std_precess.start()
#
#     load_mean_std_precess.join()
#     mean_std = mean_std_queue.get()
#
#     load_model_process.join()
#     model = model_queue.get()
#
#     print('Everything\'s loaded')


def load_evaluation_stuff():
    global mean_std, model

    mean_std = load_mean_std(None)
    model = load_model(None)
    print('Everything\'s loaded')


@torch.no_grad()
def evaluate(image: Image):
    if image.mode != 'L':
        image = image.convert('L')

    if model is None or mean_std == {}:
        raise ValueError(f'Model is not yet configured. Was in loading? {was_in_loading}')

    transformed = apply_transformations(image, mean_std)
    outputs = model(transformed.unsqueeze(0))

    probabilities = nn.Softmax(dim=0)(outputs[0])
    probabilities = map(str, probabilities.numpy())

    return dict(zip(target_names, probabilities))


# if __name__ == '__main__':
#     load_evaluation_stuff()
