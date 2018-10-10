## Dependencies 
import torch 
import numpy
import scipy.misc

import support
import networks
import torch_utils


def main():
	
	## Instantiating generator class and loading model
	generator = networks.GeneratorNet()
	generator.load_state_dict(torch.load(MODEL_FOLDER))

	## Running the sample(s) generation loop
	for sample in range(num_test_samples):

		## Generating noise to generate images out of them
		random_noise = support.noise(num_test_samples)
		generated_images = support.vectors_to_images(generator(random_noise))
		generated_images = generated_images.detach().numpy()
		
		# Save image
		scipy.misc.imsave('generated_images/gen_image_{}.jpg'.format(sample), generated_images[0][0])



if __name__ == '__main__':

	
	GEN_IMAGE = './generated_images' # folder generated images are stored
	torch_utils.Logger._make_dir(GEN_IMAGE)
	MODEL_FOLDER = 'G_epoch_199'
	num_test_samples = 5
	
	main()
