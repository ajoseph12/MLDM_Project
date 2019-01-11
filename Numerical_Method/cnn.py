import numpy as np
import time
import pickle
from matplotlib import style
import matplotlib.pyplot as plt

style.use('ggplot')

class CNN(object):


	def __init__(self, embedding, save = True):


		self.embedding = embedding
		self.train_subset_1, self.train_subset_2 = self.__baysean_error()
		self.__cnn()


	def __baysean_error(self):

		"""
		- Remove Baysean error
		- Create 2 subsets
		- Find 1NN of instances from subset 1 using subset 2
			- classify them : Delete wrongly classified instances
		-  Find 1NN of instances from subset 2 using subset 1
			- classify them : Delete wrongly classified instances
		- Repeat until stability 
		"""

		## Adding indices to the embeddings (to keep track of them)
		track_idx = np.array([i for i in range(len(self.embedding))]).reshape(-1,1)
		self.embedding  = np.concatenate((self.embedding , track_idx), axis = 1)

		## Creating subsets for CNN algo
		train_subset_1 = self.embedding[:30000]
		train_subset_2 = self.embedding[30000:60000]
		track_unwanted = list() # store irrelevant indices

		stability = False
		prev_len_subset_1 = len(train_subset_1)
		prev_len_subset_2 = len(train_subset_2)

		itr = 0
		while not stability:

			itr += 1
			print(itr)

			temp_unwanted = list()

			for n_1,sub_1 in enumerate(train_subset_1):

				eucl_dist_sorted = self.__eucl_dist(sub_1[:-2], train_subset_2)

				## Choose first k elements from sorted list 'temp_dist_idx'
				temp_first_nn = eucl_dist_sorted[0]
				temp_label = temp_first_nn[1]

				## Store indices in unwated list if class is wrong
				if temp_label != sub_1[-2]:
					temp_unwanted.append(n_1)
					track_unwanted.append(sub_1[-1])

			## Delete rows of train_subset_1 whose indices lie within the list 'temp_unwanted'  
			train_subset_1 = np.delete(train_subset_1, temp_unwanted, axis=0)

			## Save train_subset_1
			#np.save('data/train_subset_1_{}'.format(itr), train_subset_1)

			print(itr)

			temp_unwanted = list()

			for n_2,sub_2 in enumerate(train_subset_2):

				eucl_dist_sorted = self.__eucl_dist(sub_2[:-2], train_subset_1)

				## Choose first k elements from sorted list 'temp_dist_idx'
				temp_first_nn = eucl_dist_sorted[0]
				temp_label = temp_first_nn[1]

				## Store indices in unwated list if class is wrong
				if temp_label != sub_2[-2]:
					temp_unwanted.append(n_2)
					track_unwanted.append(sub_2[-1])

			## Delete rows of train_subset_1 whose indices lie within the list 'temp_unwanted'  
			train_subset_2 = np.delete(train_subset_2, temp_unwanted, axis=0)

			#np.save('data/train_subset_2_{}'.format(itr), train_subset_2)

			if prev_len_subset_1 == len(train_subset_1) and prev_len_subset_2 == len(train_subset_2):
				stability = True

			else: 
				prev_len_subset_1 = len(train_subset_1)
				prev_len_subset_2 = len(train_subset_2)


		return train_subset_1, train_subset_2


	def __cnn(self):

		"""
		- Remove instances that can be easily classified
		- Find 1NN neighbours of every instance with every other
		- if class of instance == class of other instance : Delete
		- elif class of instance != class of other instance : Keep
		"""

		## train_subset_1 union train_subset_2 
		train_emb_bay = np.concatenate((self.train_subset_1, self.train_subset_2), axis = 0)

		## Creating storage for relevant instances
		random_idx = np.random.choice(len(train_emb_bay),1)
		STORAGE = train_emb_bay[random_idx]

		stability = False

		prev_storage_len = len(STORAGE)
		itr = 0 

		while not stability:

			itr += 1
			print(itr)

			for inst in train_emb_bay:

				# Calc list sorted by ascending order of euc distance
				eucl_dist_sorted = eucl_dist(inst[:-2], STORAGE)

				# Choose first element from sorted list 'temp_dist_idx'
				temp_first_nn = eucl_dist_sorted[0]
				temp_label = temp_first_nn[1]

				# Store indices in unwated list if class is wrong
				if temp_label != inst[-2]:
					STORAGE = np.concatenate((STORAGE, inst.reshape(1,-1)), axis = 0)

				else:continue 
				#np.save('data/STORAGE_{}'.format(itr), STORAGE)

			if prev_storage_len == len(STORAGE):
				stability = True

			else:
				prev_storage_len = len(STORAGE)
				print(len(STORAGE))
				print(prev_storage_len)

		
		relevant_idx = list()
		for i in range(len(STORAGE)):
			relevant_idx.append(STORAGE[i,-1])


		with open("pickled_files/relevant_idx", "wb") as fp:   #Pickling
			pickle.dump(relevant_idx, fp)


	def __eucl_dist(self, instance, dataset):

		temp_inst = instance.reshape(1,-1)
		temp_inst = temp_inst.repeat(len(dataset), axis=0)
		eucl_dist = np.linalg.norm((temp_inst - dataset[:,:-2]), axis=1)
		eucl_dist_sorted = [(eucl_dist[i], dataset[i,-2]) for i in range(len(dataset))]
		eucl_dist_sorted.sort()

		return eucl_dist_sorted


def main():

	cnn = CNN(embedding)


if __name__ == '__main__':
	
	embedding_path = 'pickled_files/embeddings.npy'
	embedding = np.load(embedding_path)
	
	main()


