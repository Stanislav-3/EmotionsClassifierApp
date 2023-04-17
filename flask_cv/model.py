import torch.nn as nn
import torchvision.models as models


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        resnet = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        self.backbone = nn.Sequential(*list(resnet.children())[:-1])

        self.model = nn.Sequential(
            self.backbone,
            nn.Flatten(),
            nn.Dropout1d(p=0.35),
            nn.Linear(512, 256),
            nn.Dropout1d(p=0.5),
            nn.ReLU(),
            nn.Linear(256, 7)
        )

    def forward(self, x):
        return self.model(x)
