## Dependencies 
import torch 
import numpy
import scipy.misc
import argparse
from torch_utils import *
from network import *
import random
import numpy as np

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
	
	## Initializing generator class and loading model
	encoder, decoder = torch.load(MODEL_FOLDER, map_location='cpu')
	

	if MODE == "Image Gen":

		## Get image indices and images
		num_dict, images = number_dict()
		
		for i in LIST_OF_NUM:

			image_random = images[random.sample(num_dict[i], NUM_COUNT)]
			print(image_random.size())
			e_output = encoder(image_random, NUM_COUNT)
			d_output = decoder(e_output, NUM_COUNT)
			generated_images = d_output.detach().numpy()

			# Save images
			for n,image in enumerate(generated_images):
				scipy.misc.imsave('generated_images/gen_image_{}_{}.jpg'.format(i,n), image[0])

		np.save(str(save_path) + "{}".format(i), generated_images)


	elif MODE == "Embedding Gen":
		
		## Load the datasets
		train_X = torch.from_numpy(np.load(data_path + "train_X.npy"))
		train_Y = torch.from_numpy(np.load(data_path + "train_Y.npy"))
		train_Y = train_Y.unsqueeze(1)
		test_X = torch.from_numpy(np.load(data_path + "test_X.npy"))
		test_Y = torch.from_numpy(np.load(data_path + "test_Y.npy"))
		test_Y = test_Y.unsqueeze(1)
		data_list = [(train_X, train_Y), (test_X, test_Y)]

		
		## Initialize embeddings tensor
		embeddings = torch.empty(1,197)

		for n, (images, labels) in enumerate(data_list):

			batch_size = images.shape[0]
			e_output = encoder(images.float(), batch_size) #.float() otherwise an error is reporduced
			embedding = torch.cat((e_output,labels.float()), 1) #.float() otherwise an error is reporduced
			embeddings = torch.cat((embeddings, embedding))		

		embeddings = embeddings[1:] # remove the first empty/random row
		embeddings = embeddings.detach().numpy()
		np.save(emb_store_path + 'embeddings', embeddings)


	elif MODE == "Dataset Gen":

		ae_train_x = torch.from_numpy(np.load(str(data_path)+"ae_train_x.npy"))
		ae_test_x = torch.from_numpy(np.load(str(data_path)+"ae_test_x.npy"))
		
		data_list = [ae_train_x, ae_test_x]

		for n,image in enumerate(data_list):

			temp_size = image.shape[0]
			e_output = encoder(image, temp_size)
			d_output = decoder(e_output, temp_size)
			generated_images = d_output.detach().numpy()
			data = 'ae_train_x_new' if n == 0 else 'ae_test_x_new'
			np.save(str(save_path) + data, generated_images)


if __name__ == '__main__':

	MODE = 'Embedding Gen'	
	MODEL_FOLDER = 'model/demo_autoencoder.pkl'
	
	if MODE == 'Image Gen':

		## For image generating mode
		DATA_FOLDER = './torch_data/VGAN/MNIST'
		GEN_IMAGE = './generated_images' # folder generated images are stored
		make_dir(GEN_IMAGE)
		save_path ='generated_images/'
		LIST_OF_NUM = [i for i in range(10)] # list of digits to be generated
		NUM_COUNT = 2 # number of generated instances for each digit

	elif MODE == 'Embedding Gen':

		## For Encodiing mode
		EMBEDDING = './embeddings'
		make_dir(EMBEDDING)
		data_path = "Data/Data_zip/"
		emb_store_path =  "embeddings/"

	elif MODE == 'Dataset Gen':

		## For Dataset Gen mode
		data_path = 'Data/'
		save_path = 'Data/'

	main()





