## Dependencies 
import torch 
import numpy
import scipy.misc
import argparse
from torch_utils import *
from network import *
import random

"""
To-do
- Finish encoding mode
	- create a csv/pickle file with list of digits and their embeddings
- Figure out a way to name images from GANZ and combine them with
mnist and autoencoder generated images to form the train and test sets
respectively
- Finish parser function
- Try for a smaller embedding

"""
def arg_parse():

	parser = argparse.ArgumentParser(description = 'Autoencoder Inference Module')


def main():
	
	## Instantiating generator class and loading model
	encoder, decoder = torch.load(MODEL_FOLDER, map_location='cpu')

	if MODE == "Image Gen":

		## Get image indices and images
		num_dict, images = number_dict()
		
		for i in LIST_OF_NUM:

			image_random = images[random.sample(num_dict[i], NUM_COUNT)]
			e_output = encoder(image_random, NUM_COUNT)
			d_output = decoder(e_output, NUM_COUNT)
			generated_images = d_output.detach().numpy()

			# Save images
			for n,image in enumerate(generated_images):
				scipy.misc.imsave('generated_images/gen_image_{}_{}.jpg'.format(i,n), image[0])

	elif MODE == "Encoding":
		
		##### This part will have to be modified once a combined dataset is generated ####

		train_test_dataset = minst_data(DATA_FOLDER, batches = False)
		embedding_dict = dict()

		for n, data in enumerate(train_test_dataset):

			batch_size = 60000 if n == 0 else 10000
			embedding_dict[n] = list()
			loader = torch.utils.data.DataLoader(dataset=data, batch_size=batch_size,shuffle=True)
			

			for images, labels in loader:
				
				e_output = encoder(images, batch_size)
				embedding = e_output.detach().numpy()
				labels = labels.detach().numpy()
				
				embedding_dict[n].append((embedding, labels))

				break

		# Either pickle dict or save matrices in txt file
		

if __name__ == '__main__':

	
	GEN_IMAGE = './generated_images' # folder generated images are stored
	make_dir(GEN_IMAGE)
	EMBEDDING = './embeddings'
	make_dir(EMBEDDING)
	MODEL_FOLDER = 'model/demo_autoencoder.pkl'
	DATA_FOLDER = './torch_data/VGAN/MNIST'
	
	MODE = 'Encoding'
	
	## For image generating mode
	LIST_OF_NUM = [i for i in range(10)] # list of digits to be generated
	NUM_COUNT = 2 # number of generated instances for each digit


	main()





