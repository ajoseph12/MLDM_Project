## Dependencies 

import torch
from torch import nn
from torch.optim import Adam
from torch.autograd import Variable
from torchvision import transforms, datasets
from IPython import display
from support import *
from utils import *
from networks import * 



def train_discriminator(optimizer, real_data, fake_data):

	## Reset gradients
	optimizer.zero_grad()

	## Train phase on Discriminator
	# predict on real data
	prediction_real = discriminator(real_data)
	# calculate error 
	error_real = loss(prediction_real, real_data_target(real_data.size(0)))
	# back propagate
	error_real.backward()


	## Train phase on Generator
	# predict on fake data
	prediction_fake = discriminator(fake_data)
	# calculate error
	error_fake = loss(prediction_fake, fake_data_target(real_data.size(0)))
	# back propagate
	error_fake.backward()

	## Upadate weights with gradients
	optimizer.step()

	return error_real + error_fake, prediction_real, prediction_fake



def train_generator(optimizer, fake_data):

	## Reset gradients
	optimizer.zero_grad()

	## Train Generator
	# Predict using discriminator
	prediction = discriminator(fake_data)
	# calculate erro
	error = loss(prediction, real_data_target(prediction.size(0)))
	# back propagate
	error.backward()

	## Update weights with gradients
	optimizer.step()

	return error



def main():

	num_dict, images = load_data_dict()

	for i in num_dict.keys():
		temp_idx_list = num_dict[i]
		print(len(temp_idx_list))
		num_batches = len(temp_idx_list)//batch_size + 1

		
		## REINITIALIZE THE NETWORK BEFORE NEXT ITERATION BEGINS

		# Create Network instances and init weights
		generator = GenerativeNet()
		generator.apply(init_weights)

		discriminator = DiscriminativeNet()
		discriminator.apply(init_weights)

		# Enable cuda if available
		if torch.cuda.is_available():
			generator.cuda()
			discriminator.cuda()


		for epoch in range(1, num_epochs+1):    
			for n_batch in range(num_batches):
				real_batch = images[temp_idx_list[n_batch*batch_size:(n_batch*
					batch_size)+batch_size]]


				## Train Discriminator
				real_data = Variable(real_batch)
				if torch.cuda.is_available(): real_data = real_data.cuda()
				# Generate fake data
				fake_data = generator(noise(real_data.size(0))).detach()
				# Train D
				d_error, d_pred_real, d_pred_fake = train_discriminator(d_optimizer, 
					real_data, fake_data)

				## Train Generator
				# Generate fake data
				fake_data = generator(noise(real_batch.size(0)))
				# Train G
				g_error = train_generator(g_optimizer, fake_data)
				# Log error
				logger.log(d_error, g_error, epoch, n_batch, num_batches)

				## Display Progress
				if (n_batch) % 100 == 0:
					display.clear_output(True)
				# Display status Logs
				logger.display_status(epoch, num_epochs, n_batch, num_batches, 
					d_error, g_error, d_pred_real, d_pred_fake)

	if epoch % 3 == 0 and epoch != 0:
		print("Saving and Downloading......")
		torch.save(generator.state_dict(),'models/G_epoch_{}_{}'.format(i,epoch))
		torch.save(discriminator.state_dict(),'models/D_epoch_{}_{}'.format(i,epoch))


if __name__ == '__main__':

	## Logger class
	logger = Logger(model_name='DCGAN', data_name='MNIST')

	## Instantiating discriminator and generator class
	discriminator = DiscriminativeNet()
	generator = GenerativeNet()

	## Loss function
	loss = nn.BCELoss()

	## Optimizers
	d_optimizer = Adam(discriminator.parameters(), lr = 0.0002, 
		betas = (0.5, 0.999))
	g_optimizer = Adam(discriminator.parameters(), lr = 0.0002, 
		betas = (0.5, 0.999))

	## Global variables 
	num_epochs = 15
	batch_size = 16

	## Create directory for models
	dir_models = './models'
	Logger._make_dir(dir_models)


	main()