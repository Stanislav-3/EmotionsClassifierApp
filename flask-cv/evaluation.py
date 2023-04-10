import torch
from torch import nn
import json
from torchvision import transforms
from PIL import Image
from model import Net


target_names = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']


# model = Net()
# model.load_state_dict(torch.load('weights/model.pth', map_location=torch.device('cpu')))
# model.eval()

with open('weights/mean_var.json') as file:
    mean_var = json.load(file)

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Lambda(lambda image: image.repeat(3, 1, 1)),
    transforms.Normalize(mean_var['mean'], mean_var['var'])
])


@torch.no_grad()
def evaluate(image: Image):
    transformed = transform(image)

    # outputs = model(image)
    outputs = torch.rand(7)

    probabilities = nn.Softmax(dim=0)(outputs)
    probabilities = map(str, probabilities.numpy())

    return dict(zip(target_names, probabilities))


# print(evaluate(Image.open('test.jpeg')))
