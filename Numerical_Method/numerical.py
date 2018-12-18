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


	def __init__(self, image_input, embeddings_path = 'Autoencoders/embeddings/embeddings_mnist_197.npy', 
		relevant_idx_path = 'Numerical_Method/relevant_idx_197_b', 
		ae_model_path = 'Autoencoders/model/demo_autoencoder_197.pkl', k = 173, 
		matrix_m_path = "Numerical_Method/data/matrix_m_50.npy"):

		"""
		Objects instantiated on creating instance of the numerical class

		Args:
		- image_input (nd.array): numpy array of dimension 28*28
		- embeddings_path (str): path towards the train embeddings file
		- relevant_idx_path (str): path towards the list of releveant indices
		"""

		self.image_input = torch.from_numpy(image_input.reshape(1,1,28,28))
		self.embeddings_path = embeddings_path
		self.ae_model_path = ae_model_path

		self.relevant_idx = self.__relevant_idx(relevant_idx_path)
		self.embeddings = self.__get_dataset()
		self.embedding = self.__autoencoder()
		self.prediction = self.__knn(k)


	def __relevant_idx(self, relevant_idx_path):

		with open(relevant_idx_path, "rb") as fp:   # Unpickling
			relevant_idx = pickle.load(fp)
		relevant_idx = [int(i) for i in relevant_idx]

		return relevant_idx


	def __get_dataset(self):

		train_emb = np.load(self.embeddings_path)
		#train_emb = train_emb[self.relevant_idx]

		return train_emb


	def __autoencoder(self):

		encoder, decoder = torch.load(self.ae_model_path , map_location='cpu')
		batch_size = self.image_input.shape[0]

		e_output = encoder(self.image_input.float(), batch_size)
		embedding = e_output.detach().numpy()

		return embedding


	def __knn(self, k):

		## Calculate euclidean distance and sort 
		eucl_dist = np.linalg.norm((self.embedding - self.embeddings[:,:-1]), axis=1)
		eucl_dist_sorted = [(eucl_dist[i], self.embeddings[i,-1]) for i in range(len(self.embeddings))]
		eucl_dist_sorted.sort()

		## Pick first k elements
		predictions = list() 
		temp_first_k = eucl_dist_sorted[:k]
		
		count = Counter([i[1] for i in temp_first_k]) 
		for i in sorted(count.items(),key=lambda x: -x[1]): 
			predictions.append(["Prob number is {}  = {}".format(i[0], round(i[1]/k, 2))]) 
	
		
		return predictions



if __name__ == '__main__':
	
	emb_dim = 197
	k = 50
	matrix_m = "data/matrix_m.npy"

	MODEL_FOLDER = '../Autoencoders/model/demo_autoencoder_197.pkl'
	image_input = np.random.rand(28,28)
	embeddings_path = 'data/embeddings_{}_b.npy'.format(emb_dim)
	relevant_idx_path = 'relevant_idx_{}_b'.format(emb_dim)

	num = Numerical(image_input, embeddings_path, relevant_idx_path, MODEL_FOLDER, k, matrix_m)
	print(num.prediction)



"""
def __knn(self, k, matrix_m_path):

		matrix_m = np.load(matrix_m_path)

		## Calculate euclidean distance and sort 
		temp_inst = self.embedding.reshape(1,-1)
		temp_inst = temp_inst.repeat(len(self.dataset), axis=0)
		difference = temp_inst - self.dataset[:,:-1]
		eucl_dist = np.diag(np.sqrt(np.matmul(np.matmul(difference, matrix_m),difference.T)))
		eucl_dist_sorted = [(eucl_dist[i], self.dataset[i,-1]) for i in range(len(self.dataset))]
		eucl_dist_sorted.sort()

		## Pick first k elements
		predictions = list() 
		temp_first_k = eucl_dist_sorted[:k]
		
		count = Counter([i[1] for i in temp_first_k]) 
		for i in sorted(count.items(),key=lambda x: -x[1]): 
			predictions.append(["Prob number is {}  = {}".format(i[0], i[1]/k )]) 
	
		
		return predictions

def __knn(self, k):

		## Calculate euclidean distance and sort 
		eucl_dist = np.linalg.norm((self.embedding - self.dataset[:,:-1]), axis=1)
		eucl_dist_sorted = [(eucl_dist[i], self.dataset[i,-1]) for i in range(len(self.dataset))]
		eucl_dist_sorted.sort()

		## Pick first k elements
		predictions = list() 
		temp_first_k = eucl_dist_sorted[:k]
		
		count = Counter([i[1] for i in temp_first_k]) 
		for i in sorted(count.items(),key=lambda x: -x[1]): 
			predictions.append(["Prob number is {}  = {}".format(i[0], i[1]/k )]) 
	
		
		return predictions
"""

