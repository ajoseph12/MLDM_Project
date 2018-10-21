import torch 
from torch import nn, optim
from torch.autograd.variable import Variable
from torchvision import transforms, datasets


def minst_data(DATA_FOLDER, batch_size, download = False):

	compose = transforms.Compose([transforms.ToTensor(), 
		transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

	out_dir = '{}/dataset'.format(DATA_FOLDER)

	train_test_dataset = [datasets.MNIST(root = out_dir, train = True, transform = compose,
		download = download), datasets.MNIST(root = out_dir, train = False, 
		transform = compose, download = download)]

	train_loader = torch.utils.data.DataLoader(dataset=train_test_dataset[0],
		batch_size=batch_size,shuffle=True)
	test_loader = torch.utils.data.DataLoader(dataset=train_test_dataset[1],
		batch_size=batch_size,shuffle=True)

	train_test_data = [train_loader, test_loader]

	return train_test_data
