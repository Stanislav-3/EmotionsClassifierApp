import torch.nn as nn


class Net(nn.Module):
    def __init__(self, backbone):
        super(Net, self).__init__()

        # last layer
        backbone.fc = nn.Linear(backbone.fc.in_features, 7, bias=True)

        self.model = nn.Sequential(
            # mapping grayscale pictures to 3 channels
            nn.Conv2d(1, 3, 1),
            backbone
        )

        # for param in self.model[1].parameters():
        #   param.requires_grad = False

    def forward(self, x):
        return self.model(x)