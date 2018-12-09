import sys
import torch
import numpy
import scipy.misc
import pickle
import random
import numpy as np
sys.path.append("..")
from Autoencoders.network import *
from Autoencoders.torch_utils import *




class Numerical(object):


	def __init__(self, image_input, dataset_path = 'Numerical_Method/data/embeddings_197.npy', relevant_idx_path = 'Numerical_Method/relevant_idx',
		ae_model_path = 'Autoencoders/model/demo_autoencoder_197.pkl', k = 50):

		"""
		Objects instantiated on creating instance of the numerical class

		Args:
		- image_input (nd.array): numpy array of dimension 28*28
		- dataset_path (str): path towards the train embeddings file
		- relevant_idx_path (str): path towards the list of releveant indices
		"""

		self.image_input = torch.from_numpy(image_input.reshape(1,1,28,28))
		self.dataset_path = dataset_path
		self.ae_model_path = ae_model_path

		self.relevant_idx = self.__relevant_idx(relevant_idx_path)
		self.dataset = self.__get_dataset()
		self.embedding = self.__autoencoder()
		self.prediction = self.__knn(k)


	def __relevant_idx(self, relevant_idx_path):

		with open(relevant_idx_path, "rb") as fp:   # Unpickling
			relevant_idx = pickle.load(fp)
		relevant_idx = [int(i) for i in relevant_idx]

		return relevant_idx
		emb_train = emb[relevant_idx]


	def __get_dataset(self):

		train_emb = np.load(self.dataset_path)
		train_emb = train_emb[self.relevant_idx]

		return train_emb


	def __autoencoder(self):

		encoder, decoder = torch.load(self.ae_model_path , map_location='cpu')
		batch_size = self.image_input.shape[0]

		e_output = encoder(self.image_input.float(), batch_size)
		embedding = e_output.detach().numpy()

		return embedding


	def __knn(self, k):

		## Calculate euclidean distance and sort 
		eucl_dist = np.linalg.norm((self.embedding - self.dataset[:,:-1]), axis=1)
		eucl_dist_sorted = [(eucl_dist[i], self.dataset[i,-1]) for i in range(len(self.dataset))]
		eucl_dist_sorted.sort()

		## Pick first k elements
		temp_first_k = eucl_dist_sorted[:k]
		temp_labels = [digit[1] for digit in temp_first_k]

		## Pick label that has majority count and append to prediction list
		temp_list = [temp_labels.count(i) for i in temp_labels]
		prediction = temp_labels[temp_list.index(max(temp_list))]
		
		return prediction


if __name__ == '__main__':
	
	emb_dim = 197
	k = 50

	MODEL_FOLDER = '../Autoencoders/model/demo_autoencoder_197.pkl'
	image_input = np.random.rand(28,28)
	dataset_path = 'data/embeddings_{}.npy'.format(emb_dim)
	relevant_idx_path = 'relevant_idx'

	num = Numerical(image_input, dataset_path, relevant_idx_path, MODEL_FOLDER, k)
	print(num.prediction)





