## Dependencies
from IPython import display
import torch 
from torch import nn, optim
from torch.autograd.variable import Variable

import support
import networks
import torch_utils


def real_data_target(size):

	"""Tensor of ones with shape = size, as real-images targets 
	are always ones"""

	data = Variable(torch.ones(size, 1))
	if torch.cuda.is_available(): return data.cuda()
	return data


def fake_data_target(size):

	"""Tensor of zeros, with shape = size, as fake-images targets
	are always zero"""

	data = Variable(torch.zeros(size, 1))
	if torch.cuda.is_available(): return data.cuda()
	return data


def train_discriminator(optimizer, real_data, fake_data):

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
	error_fake = loss(prediction_fake, fake_data_target(real_data.size(0)))
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
	error = loss(prediction, real_data_target(prediction.size(0)))
	error.backward()

	# Update weights with gradients
	optimizer.step

	return error


def main():

	
	## Generating samples for testing
	num_test_samples = 16
	test_noise = support.noise(num_test_samples)

	## Instantiating the Logger class
	logger = torch_utils.Logger(model_name = "Vanilla GANs", data_name = 'MNIST')

	## Running the training loop
	for epoch in range(EPOCHS):
		for n_batch, (real_batch, _) in enumerate(data_loader):

			## Part 1 - Training the discriminator 
			# Reformatting real data ((100,1,28,28) --> (100, 784))
			real_data = Variable(support.images_to_vectors(real_batch))
			if torch.cuda.is_available(): real_data = real_data.cuda()
			# Generating fake data (detach detaches o/p from the comp graph - no backprop)
			fake_data = generator(support.noise(real_data.size(0))).detach()
			# Training the discriminator 
			d_error, d_pred_real, d_pred_fake = train_discriminator(d_optimizer, 
				real_data, fake_data)

			## Part 2 - Training the generator
			# Generate fake data
			fake_data = generator(support.noise(real_batch.size(0)))
			# Training the generator
			g_error = train_generator(g_optimizer, fake_data)
			

			## Error logger
			logger.log(d_error, g_error, epoch, n_batch, num_batches)

			## Display the Progress
			if (n_batch) % 100 == 0:
				display.clear_output(True)

				# Display Images
				test_images = support.vectors_to_images(generator(test_noise)).data.cpu()
				logger.log_images(test_images, num_test_samples, epoch, n_batch, 
					num_batches);

				# Display status Logs
				logger.display_status(epoch, EPOCHS, n_batch, num_batches, d_error, 
					g_error, d_pred_real, d_pred_fake)

			# Model Checkpoints
			logger.save_models(generator, discriminator, epoch)




if __name__ == '__main__':

	
	D_STEPS = 1 # Number of steps to apply to discriminator 
	EPOCHS = 200
	LR = 0.002
	DATA_FOLDER = './torch_data/VGAN/MNIST' # folder in which MINST is stored

	## Data preparation 
	data = support.minst_data(DATA_FOLDER) # Load data
	# Create loader with data so that we can iterate over it
	data_loader = torch.utils.data.DataLoader(data, batch_size = 100, shuffle = True)
	num_batches = len(data_loader)


	## D and G class instances 
	discriminator = networks.DiscriminatorNet()
	generator = networks.GeneratorNet()

	## Optimizers
	d_optimizer = optim.Adam(discriminator.parameters(), LR)
	g_optimizer = optim.Adam(generator.parameters(), LR)

	## Loss function
	loss = nn.BCELoss() # Binary cross entropy loss function

	main()