import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR

from core.microX_models import eyeNet, noseNet, mouthNet


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if __name__ == "__main__":
    # complete image
    # Break image down to microexpression components (eyes, nose, mouth)
    # feed each of the microexpresson components of size 30x30 through their own models
    # with the output from each model, use a naive bayes model approach to get the overall classification
    
    print("MicroX Initialised")

    eyePolicy = eyeNet()
    nosePolicy = noseNet()
    mouthPolicy = mouthNet()

    policies = [eyePolicy, nosePolicy, mouthPolicy]

    for policy in policies:
        policy.to(DEVICE)
        policy.eval()

        test_loss = 0
        correct = 0
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
                pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
                correct += pred.eq(target.view_as(pred)).sum().item()

        test_loss /= len(test_loader.dataset)

        print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
            test_loss, correct, len(test_loader.dataset),
            100. * correct / len(test_loader.dataset)))
