import numpy as np
import copy
from PIL import Image
from io import BytesIO
import torch
from torchvision import transforms
from torchvision.utils import save_image
import torch.nn as nn
import torchvision.models as models
from .nets import Net


def load_image_into_numpy_array(data):
    img = Image.open(BytesIO(data))
    return np.array(img)


transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Grayscale(num_output_channels=1)
    ])


def predict(image):
    image = copy.deepcopy(image)
    image = load_image_into_numpy_array(image.read())

    # if png remove 4th channel
    if image.shape[-1] == 4:
        image = np.delete(image, -1, axis=2)

    image = transform(image)
    save_image(image, 'media/gray.jpg')

    image = transforms.CenterCrop(min(image.shape[1:]))(image)
    image = transforms.Resize(48)(image)

    save_image(image, 'media/transformed.jpg')

    model = Net(models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1))
    model.load_state_dict(torch.load('static/models/model.pth',
                                     map_location=torch.device('cpu')))

    outputs = model(image.unsqueeze(0))
    probabilities = nn.Softmax(dim=1)(outputs).detach()
    probabilities = probabilities.numpy()[0]
    return probabilities

