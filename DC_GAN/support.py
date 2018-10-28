
## Dependencies 

import torch
from torch import nn
from torch.optim import Adam
from torch.autograd import Variable
from torchvision import transforms, datasets
from IPython import display


def real_data_target(size):

	"""Tensor containing ones, with shape = size"""

	data = Variable(torch.ones(size, 1))
	if torch.cuda.is_available(): return data.cuda()
	return data 


def fake_data_target(size):

	"""Tensor containing zeros with shape = size"""

	data = Variable(torch.zeros(size, 1))
	if torch.cuda.is_available(): return data.cuda()
	return data


def noise(size):
    n = Variable(torch.randn(size, 100))
    if torch.cuda.is_available(): return n.cuda()
    return n


def init_weights(m):

	classname = m.__class__.__name__
	if classname.find('Conv') != -1 or classname.find('BatchNorm') != -1:
		m.weight.data.normal_(0.00, 0.02)


def load_data_dict(path = './torch_data/VGAN/MNIST/dataset'):

	compose = transforms.Compose([transforms.Resize(64), 
		transforms.ToTensor(), transforms.Normalize((.5, .5, .5), 
			(.5, .5, .5))])

	train_dataset = datasets.MNIST(root = path, train = True, transform = 
		compose, download = False)
	train_loader = torch.utils.data.DataLoader(dataset = train_dataset,
		batch_size = 60000, shuffle = True)
	test_dataset = datasets.MNIST(root = path, train = False, transform = 
		compose, download = False)
	test_loader = torch.utils.data.DataLoader(dataset = test_dataset,
		batch_size = 10000, shuffle = True)

	data_list = [train_loader, test_loader]

	num_idx_dict = dict()
	images = list()
	for i in range(10): num_idx_dict[i] = list()

	index = 0 
	for data in data_list:
		for image, labels in data:
			for l in labels:
				num_idx_dict[int(l.numpy())].append(index)
				index+=1

			images.append(image)

	image_concat = torch.cat((images[0], images[1]), 0)
	return num_idx_dict, image_concat


