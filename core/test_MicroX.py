import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR

from core.microX_models import eyeNet, noseNet, mouthNet

def test(policy, device, data):
    policy.to(DEVICE)
    policy.eval()

    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in data:
            data, target = data.to(device), target.to(device)
            output = policy(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(data.dataset)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(data.dataset),
        100. * correct / len(data.dataset)))


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if __name__ == "__main__":  
    print("MicroX Initialised")

    print("Data Loading...")
    # insert function for dataloader
    data = None

    eyePolicy = eyeNet()
    nosePolicy = noseNet()
    mouthPolicy = mouthNet()

    policies = [eyePolicy, nosePolicy, mouthPolicy]

    for policy in policies:
        test(policy, DEVICE, data)

