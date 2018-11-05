import torch 
from torch import nn, optim
from torch.autograd.variable import Variable
from torchvision import transforms, datasets
import errno
import os

def minst_data(DATA_FOLDER, batch_size = 100, download = False, batches = True):

	compose = transforms.Compose([transforms.ToTensor(), 
		transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

	out_dir = '{}/dataset'.format(DATA_FOLDER)

	train_test_dataset = [datasets.MNIST(root = out_dir, train = True, transform = compose,
		download = download), datasets.MNIST(root = out_dir, train = False, 
		transform = compose, download = download)]

	if batches == True:
		train_loader = torch.utils.data.DataLoader(dataset=train_test_dataset[0],
			batch_size=batch_size,shuffle=True)
		test_loader = torch.utils.data.DataLoader(dataset=train_test_dataset[1],
			batch_size=batch_size,shuffle=True)

		train_test_data = [train_loader, test_loader]

		return train_test_data

	else : return train_test_dataset


def make_dir(directory):

	if not os.path.isdir(directory):

		try:
			os.makedirs(directory)

		except OSError as e:
			if e.errno != errno.EEXIST:
				raise


def number_dict(batch_size = 30000, path = './Data/torch_data/VGAN/MNIST/dataset'):

	train_dataset = datasets.MNIST(root=path, train=True,transform=transforms.ToTensor(),
		download= False)

	train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, 
		shuffle=True)

	num_idx_dict = dict()
	for i in range(10):num_idx_dict[i] = list()

	for image, labels in train_loader:
		for n,l in enumerate(labels):
			num_idx_dict[int(l.numpy())].append(n)
		break

	return num_idx_dict, image

