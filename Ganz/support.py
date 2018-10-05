import torch 
from torch import nn, optim
from torch.autograd.variable import Variable
from torchvision import transforms, datasets


DATA_FOLDER = './torch_data/VGAN/MNIST'

def minst_data():

	compose = transforms.Compose([transforms.ToTensor(), 
		transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

	out_dir = '{}/dataset'.format(DATA_FOLDER)
	return datasets.MNIST(root = out_dir, train = True, transform = compose,
		download = True)


