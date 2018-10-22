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
- Finish parser function

"""
def arg_parse():

	parser = argparse.ArgumentParser(description = 'Autoencoder Inference Module')


def main():
	
	## Instantiating generator class and loading model
	#encoder = Encoder()
	#decoder = Decoder()
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

	if mode == "Encoding":
		pass
		


if __name__ == '__main__':

	
	GEN_IMAGE = './generated_images' # folder generated images are stored
	make_dir(GEN_IMAGE)
	MODEL_FOLDER = 'model/demo_autoencoder.pkl'
	
	MODE = 'Image Gen'
	
	## For image generating mode
	LIST_OF_NUM = [i for i in range(10)] # list of digits to be generated
	NUM_COUNT = 2 # number of generated instances for each digit


	main()





