import torch 
from torch import nn, optim



# GLOBAL VARIABLES
HIDDEN_UNITS = [1024, 512, 256]
NEGSLOPE_LRELU = [0.2, 0.2, 0.2] # -ve relu slopes (same for G and D)
DROPOUT = [0.3, 0.3, 0.3]


class DiscriminatorNet(torch.nn.Module):

	"""
	A three hidden-layer discriminative neural network
	"""

	def __init__(self):

		super().__init__()

		n_features = 784 # 28*28 images
		n_out = 1

		# Hidden-layer definitions
		self.hidden_0 = nn.Sequential(nn.Linear(n_features, HIDDEN_UNITS[0]),
			nn.LeakyReLU(NEGSLOPE_LRELU[0]), nn.Dropout(DROPOUT[0]))

		self.hidden_1 = nn.Sequential(nn.Linear(HIDDEN_UNITS[0], HIDDEN_UNITS[1]),
			nn.LeakyReLU(NEGSLOPE_LRELU[1]), nn.Dropout(DROPOUT[1]))

		self.hidden_2 = nn.Sequential(nn.Linear(HIDDEN_UNITS[1], HIDDEN_UNITS[2]),
			nn.LeakyReLU(NEGSLOPE_LRELU[2]), nn.Dropout(DROPOUT[2]))

		self.out = nn.Sequential(nn.Linear(HIDDEN_UNITS[2], n_out), nn.Sigmoid())


	def forward(self, x):

		# Forward pass
		x = self.hidden_0(x)
		x = self.hidden_1(x)
		x = self.hidden_2(x)
		x = self.out(x)

		return x




class GeneratorNet(torch.nn.Module):

	"""
	A three hidden-layer generative neural network
	"""

	def __init__(self):
		super().__init__()

		n_features = 100
		n_out = 784

		self.hidden_0 = nn.Sequential(nn.Linear(n_features,HIDDEN_UNITS[2]), 
			nn.LeakyReLU(NEGSLOPE_LRELU[0]))

		self.hidden_1 = nn.Sequential(nn.Linear(HIDDEN_UNITS[2], HIDDEN_UNITS[1]),
			nn.LeakyReLU(NEGSLOPE_LRELU[1]))

		self.hidden_2 = nn.Sequential(nn.Linear(HIDDEN_UNITS[1], HIDDEN_UNITS[0]),
			nn.LeakyReLU(NEGSLOPE_LRELU[2]))

		self.out = nn.Sequential(nn.Linear(HIDDEN_UNITS[0], n_out), nn.Tanh())

	
	def forward(self, x):

		x = self.hidden_0(x)
		x = self.hidden_1(x)
		x = self.hidden_2(x)
		x = self.out(x)

		return x










