
## Dependencies
from torch_utils import *
from network import * 
import torch
import torch.nn as nn
import torch.utils as utils
from tqdm import tqdm


def main():

	noise = torch.rand(BATCH_SIZE, 1, 28, 28) # random noise

	for epoch in range(EPOCHS):

		for dataset in datasets:

			for image, labels in tqdm(dataset):

				image = Variable(image) #.cuda()
				image_noise = torch.add(image, N_FACTOR*noise)
				image_noise = Variable(image_noise) #.cuda()

				optimizer.zero_grad()
				e_output = encoder(image_noise, BATCH_SIZE)
				d_output = decoder(e_output, BATCH_SIZE)
				loss = loss_func(d_output, image)
				loss.backward()
				optimizer.step()

		torch.save([encoder, decoder], SAVE_PATH)
		print(loss)


if __name__ == '__main__':

	## Global Initializations
	LR = 0.0005 # learning rate
	N_FACTOR = 0.4 # noise factor 
	BATCH_SIZE = 100
	EPOCHS = 10
	DATA_PATH = './torch_data/VGAN/MNIST' # data save/load path
	SAVE_PATH = './model/demo_autoencoder.pkl' # model save path

	## Load datasets
	datasets = minst_data(DATA_PATH, BATCH_SIZE)

	## Initializations of the network
	encoder = Encoder() #.cuda()
	decoder = Decoder() #.cuda()

	## Parameters, loss functiona and optimizer 
	parameters = list(encoder.parameters()) + list(decoder.parameters())
	loss_func = nn.MSELoss()
	optimizer = torch.optim.Adam(parameters, lr=LR)
	

	main()



	