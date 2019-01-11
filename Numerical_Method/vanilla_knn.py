import numpy as np
import time
import pickle
from matplotlib import style
import matplotlib.pyplot as plt

style.use('ggplot')

class Vanilla_KNN(object):

	
	def __init__(self, embedding, k_test, time = False, save = False, plot = False):


		self.time = time
		self.save = save

		self.emb_train = embedding[:60000]
		self.emb_test = embedding[60000:]
		self.k_test = k_test
		self.predictions = self.__knn()
		
		if plot:self.__plot()

	
	def __knn(self):

		predictions = dict()
		for k in range(1,k_test+1) : predictions[k] = list()

		time_list = list()
		start_time = time.time()
		

		for n,test_inst in enumerate(self.emb_test):

			instance = test_inst[:-1] # remove the label
			temp_dist_idx = self.__eucl_dist(instance, self.emb_train) # dataset = emb_train 


			for k in range(1,self.k_test+1):

				## Choose first k elements from sorted list 'temp_dist_idx'
				temp_first_k = temp_dist_idx[:k]
				temp_labels = [digit[1] for digit in temp_first_k]

				## Pick label that has majority count and append to prediction list
				temp_list = [temp_labels.count(i) for i in temp_labels]
				predictions[k].append(temp_labels[temp_list.index(max(temp_list))])

			time_list.append(round(time.time() - start_time,3))
			print(n, round(time.time() - start_time,3))

		
		if self.save:

			## Pickling predictions and time values
			path = "data/"
			with open(path + "predictions_knn" + '.pkl', 'wb') as f:
				pickle.dump(predictions, f, pickle.HIGHEST_PROTOCOL)

			with open(path + "time_knn" + '.pkl', 'wb') as f:
				pickle.dump(time_list, f, pickle.HIGHEST_PROTOCOL)

		return 


	def __eucl_dist(self, instance, dataset):

		temp_inst = instance.reshape(1,-1)
		eucl_dist = np.linalg.norm((temp_inst - dataset[:,:-1]), axis=1)
		eucl_dist_sorted = [(eucl_dist[i], dataset[i,-1]) for i in range(len(dataset))]
		eucl_dist_sorted.sort()

		return eucl_dist_sorted


	def __plot(self):

		accuracy = list()

		for k in range(1, self.k_test+1):
			sim_pred = sum(self.predictions[k] == self.emb_test[:,-1])
			accuracy.append((sim_pred/len(self.emb_test),k))

		## Plotting accuracy (y_axis) vs K value (x_axis) curve
		acc_k = [val[1] for val in accuracy]
		acc_val = [val[0] for val in accuracy]

		plt.plot(acc_k, acc_val)
		plt.show()




def main():


	knn = Vanilla_KNN(embedding, k_test, time = False, save = False)


if __name__ == '__main__':

	embedding_path = 'pickled_files/embeddings.npy'
	embedding = np.load(embedding_path)
	k_test = 200

	main()



