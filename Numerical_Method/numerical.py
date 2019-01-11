import sys
import torch
import numpy
import scipy.misc
import pickle
import random
import numpy as np
from collections import Counter
sys.path.append("..")
from Autoencoders.network import *
from Autoencoders.torch_utils import *




class Numerical(object):


	def __init__(self, image_input, dataset_path = './Autoencoders/embeddings/embeddings_197_b.npy', 
		relevant_idx_path = './Numerical_Method/relevant_idx_197_b', 
		ae_model_path = './Autoencoders/model/demo_autoencoder_197_b.pkl', k = 48, metric = False):

		"""
		Objects instantiated on creating instance of the numerical classr

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
		self.prediction = self.__knn(k, metric)


	def __relevant_idx(self, relevant_idx_path):

		with open(relevant_idx_path, "rb") as fp:   # Unpickling
			relevant_idx = pickle.load(fp)
		relevant_idx = [int(i) for i in relevant_idx]

		return relevant_idx


	def __get_dataset(self):

		train_emb = np.load(self.dataset_path)
		# train_emb = train_emb[self.relevant_idx]

		return train_emb


	def __autoencoder(self):

		encoder, decoder = torch.load(self.ae_model_path , map_location='cpu')
		batch_size = self.image_input.shape[0]

		e_output = encoder(self.image_input.float(), batch_size)
		embedding = e_output.detach().numpy()

		return embedding


	def __knn(self, k, metric):

		## Calculate euclidean distance and sort 
		if not metric:
			eucl_dist = np.linalg.norm((self.embedding - self.dataset[:,:-1]), axis=1)
			eucl_dist_sorted = [(eucl_dist[i], self.dataset[i,-1]) for i in range(len(self.dataset))]
			eucl_dist_sorted.sort()

			
		elif metric:

			## Load the computed metric
			matrix_m = np.load('./Numerical_Method/matrix_m_40_b.npy')

			## Calculate the distance of each test instance from train instances 
			eucl_dist_sorted = self.__eucl_dist_metric(self.embedding, self.dataset, matrix_m)


		## Pick first k elements
		predictions = list() 
		temp_first_k = eucl_dist_sorted[:k]

		## Percentage prediction of each number
		count = Counter([i[1] for i in temp_first_k]) 
		for i in sorted(count.items(),key=lambda x: -x[1]): 
			predictions.append([str(i[0]), str(i[1]/k)]) 

		
		return predictions


	def __eucl_dist_metric(self, instance, dataset, matrix_m):
		"""Calculates eucl dist for metric case"""

		temp_inst = instance.reshape(1,-1)
		temp_inst = temp_inst.repeat(len(dataset), axis=0)
		difference = temp_inst - dataset[:,:-1]
		eucl_dist = np.diag(np.sqrt(np.matmul(np.matmul(difference, matrix_m),difference.T)))
		eucl_dist_sorted = [(eucl_dist[i], dataset[i,-1]) for i in range(len(dataset))]
		eucl_dist_sorted.sort()

		return eucl_dist_sorted



if __name__ == '__main__':
	
	emb_dim = 197
	k = 48

	MODEL_FOLDER = '../Autoencoders/model/demo_autoencoder_197_b.pkl'
	image_input = np.random.rand(28,28)
	dataset_path = '../Autoencoders/embeddings/embeddings_{}_b.npy'.format(emb_dim)
	relevant_idx_path = 'relevant_idx_{}_b'.format(emb_dim)
	metric = True

	num = Numerical(image_input, dataset_path, relevant_idx_path, MODEL_FOLDER, k,metric)
	print(num.prediction)





