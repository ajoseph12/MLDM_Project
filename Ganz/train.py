import torch 
from torch import nn, optim
import support
import networks


def real_data_target(size):

	"""Tensor of ones with shape = size as real-images targets 
	are always ones"""

	data = Variable(torch.ones(size, 1))
	if torch.cuda.is_available(): return data.cuda()

	return data


def fake_data_target(size):

	"""Tensor of zeros, with shape = size as fake-images targets
	are always zero"""

	data = Variable(torch.zeros(size, 1))
	if torch.cuda.is_available(): return data.cuda()


def train_discriminator(optimizers, real_data, fake_data):

	# Reset gradients
	optimizer.zero_grad()

	# Train on real data (NOT SURE ABOUT WORKING!!!)
	prediction_real = discriminator(real_data) 
	# Calculate the error and backpropagate
	error_real = loss(prediction_real, real_data_target(real_data.size(0)))
	error_real.backward()

	# Train on fake data
	prediction_fake = discriminator(fake_data)
	# Calculate the error and backpropagate
	error_fake = loss(prediction_real, fake_data_target(real_data.size(0)))
	error_fake.backward()

	# Update weights with gradient 
	optimizer.step()

	return error_real + error_fake, prediction_real, prediction_fake


def train_generator(optimizer, fake_data):

	# Reset gradients
	optimizer.zero_grad()

	# sample noise and generate fake data
	prediction = discriminator(fake_data)
	# Calculate error and backpropagate
	error = loss(prediction, real_data_target(real_data.size(0)))
	error.backwards()

	# Update weights with gradients
	optimizer.step

	return error





def main():

	D_STEPS = 1 # Number of steps to apply to discriminator 
	EPOCHS = 200
	LR = 0.002


	# D and G class instances 
	discriminator = networks.DiscriminatorNet()
	generator = networks.GeneratorNet()

	# Optimizers
	d_optimizer = optim.Adam(discriminator.parameters(), LR)
	g_optimizer = optim.Adam(generator.parameters(), LR)

	loss = nn.BCEloss() # Binary cross entropy loss function





if __name__ == '__main__':


	main()