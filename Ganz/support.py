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


def images_to_vectors(images):

	return images.view(images.size(0), 784)


def vectors_to_images(vectors):

	return vectors.view(vectors.size(0), 1, 28, 28)


def noise(size):

	n = Variable(torch.randn(size, 100))
	if torch.cuda.is_available(): return n.cuda()
	return n
