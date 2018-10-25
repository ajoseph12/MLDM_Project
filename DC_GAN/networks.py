import torch 
from torch import nn, optim


class DiscriminativeNet(torch.nn.Module):

	def __init__(self):
		super().__init__()

		self.conv1 = nn.Sequential(nn.Conv2d(in_channels = 1,
			out_channels = 128, kernel_size = 4, stride = 2, padding = 1,
			bias = False), nn.LeakyReLU(0.2, inplace = True))

		self.conv2 = nn.Sequential(nn.Conv2d(in_channels = 128,
			out_channels = 256, kernel_size = 4, stride = 2, padding = 1,
			bias = False), nn.BatchNorm2d(256), nn.LeakyReLU(0.2, inplace = True))

		self.conv3 = nn.Sequential(nn.Conv2d(in_channels = 256,
			out_channels = 512, kernel_size = 4, stride = 2, padding = 1, 
			bias = False), nn.BatchNorm2d(512), nn.LeakyReLU(0.2, inplace = True))

		self.conv4 = nn.Sequential(nn.Conv2d(in_channels = 512, 
			out_channels = 1024, kernel_size = 4, stride = 2, padding = 1,
			bias = False), nn.BatchNorm2d(1024), nn.LeakyReLU(0.2, inplace = True))

		self.out = nn.Sequential(nn.Linear(1024*4*4, 1), nn.Sigmoid())


	def forward(self, x):

		## Convolutional layers
		x = self.conv1(x)
		x = self.conv2(x)
		x = self.conv3(x)
		x = self.conv4(x)

		## Flatten and apply sigmoid
		x = x.view(-1, 1024*4*4)
		x = self.out(x)

		return x



class GenerativeNet(torch.nn.Module):

	def __init__(self):
		super().__init__()

		self.linear = torch.nn.Linear(100, 1024*4*4)

		self.conv1 = nn.Sequential(nn.ConvTransposed2d(in_channels = 1024,
			out_channels = 256, kernel_size = 4, stride = 2, padding = 1,
			bias = False), nn.BatchNorm())

		self.conv2 = nn.Sequential(nn.ConvTransposed2d)

test = torch.randn((10,1,64,64))
print(test.size())
d = DiscriminativeNet()
d(test)

