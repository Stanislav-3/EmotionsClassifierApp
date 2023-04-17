import torch.nn as nn
import torchvision.models as models


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        resnet = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        self.backbone = nn.Sequential(*list(resnet.children())[:-2])

        self.model = nn.Sequential(
            self.backbone,

            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),

            nn.AdaptiveAvgPool2d(output_size=(1, 1)),
            nn.Flatten(),
            #         nn.Dropout1d(p=0.2),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            #         nn.Dropout1d(p=0.2),
            nn.ReLU(),
            nn.Linear(256, 7)
        )

    def forward(self, x):
        return self.model(x)
