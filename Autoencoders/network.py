## Dependencies
import torch
import torch.nn as nn
import torch.utils as utils
from torch.autograd import Variable
import torchvision.datasets as dset
import torchvision.transforms as transforms
import matplotlib.pyplot as plt


## Encoder Network
class Encoder(nn.Module):
	
	"""
	Output datastructure :
		- Input 	- 28*28*1
		- layer 1	- 28*28*16	(conv)
		- layer 2 	- 14*14*8	(conv and then maxpool)
		- layer 3	- 7*7*4		(conv and then maxpool)
	"""

	def __init__(self):
		
		super(Encoder,self).__init__()
		
		self.layer_1 = nn.Sequential(nn.Conv2d(1,16,3,padding=1),nn.ReLU(),
			nn.BatchNorm2d(16))
		self.layer_2 = nn.Sequential(nn.Conv2d(16,8,3,padding=1), nn.ReLU(),
			nn.BatchNorm2d(8),nn.MaxPool2d(2,2))
		self.layer_3 = nn.Sequential(nn.Conv2d(8,4,3,padding=1), nn.ReLU(),
			nn.BatchNorm2d(4),nn.MaxPool2d(2,2))


	def forward(self,x, batch_size):

		x = self.layer_1(x)
		x = self.layer_2(x)
		out = self.layer_3(x)
		out = out.view(batch_size, -1)
		return out


## Decoder Network

class Decoder(nn.Module):
	
	"""

	Output datastructure :
		- Input 	- 7*7*4
		- layer 1	- 13*13*8	(convtranspose)
		- layer 2 	- 26*26*16	(convtranspose)
		- layer 3	- 28*28*1	(conv )
	"""

	def __init__(self):
		
		super(Decoder,self).__init__()
		
		self.layer_1 = nn.Sequential(nn.ConvTranspose2d(4,8,3,stride=2,padding=1), nn.ReLU(),
			nn.BatchNorm2d(8))
		self.layer_2 = nn.Sequential(nn.ConvTranspose2d(8,16,3,stride=2,padding=1, output_padding=1), 
			nn.ReLU(),nn.BatchNorm2d(16))
		self.layer_3 = nn.Sequential(nn.ConvTranspose2d(16,1,3), nn.ReLU())

	def forward(self,x, batch_size):

		x = x.view(batch_size,4,7,7)
		x = self.layer_1(x)
		x = self.layer_2(x)
		out = self.layer_3(x)
		return out











