## Dependencies 
import torch 
import numpy
import scipy.misc

from support import *
from networks import *
from utils import *


def main():
	
	## Instantiating generator class and loading model
	generator = GenerativeNet()
	generator.load_state_dict(torch.load(MODEL_FOLDER, map_location=lambda storage, loc: storage))

	if MODE == 'Image Gen':
		## Generating noise to generate images out of them
		random_noise = noise(num_test_samples)
		generated_images = generator(random_noise)
		generated_images = generated_images.detach().numpy()
		print(generated_images.shape)

		for i in range(10):
			scipy.misc.imsave('generated_images/gen_image_{}.jpg'.format(i), generated_images[i][0])
		
	elif MODE == 'Dataset Gen':

		for i in range(10):

			generator.load_state_dict(torch.load('data/drive/G_epoch_{}_30'.format(i), 
				map_location=lambda storage, loc: storage))
			## Generating noise to generate images out of them
			random_noise = noise(num_test_samples)
			generated_images = generator(random_noise)
			generated_images = generated_images.detach().numpy()
			np.save(str(save_path) + '{}'.format(i), generated_images)



if __name__ == '__main__':

	MODE = 'Dataset Gen'
	num_test_samples = 1250


	## For Image Gen part
	GEN_IMAGE = './generated_images' # folder generated images are stored
	Logger._make_dir(GEN_IMAGE)
	MODEL_FOLDER = 'data/drive/G_epoch_0_30'
	

	## For Dataset Gen part
	save_path = 'data/'


	main()
