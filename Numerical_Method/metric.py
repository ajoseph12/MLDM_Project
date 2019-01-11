import numpy as np
import time
import pickle
from matplotlib import style
import matplotlib.pyplot as plt
import metric_learn

style.use('ggplot')



class Metric(object):


	def __init__(self, relevant_idx_path, embedding, metric_k, k_test, plot = True):

		self.metric_k = metric_k
		self.embedding = embedding
		self.k_test = k_test
		self.emb_train = self.__strong_instance(relevant_idx_path, embedding)
		self.predictions = self.__matrix_m()

		if plot:self.__plot()

	
	def __strong_instance(self, relevant_idx_path, embedding):

		with open(relevant_idx_path, "rb") as fp:   
			relevant_idx = pickle.load(fp)

		relevant_idx = [int(i) for i in relevant_idx]
		emb_train = self.embedding[relevant_idx]

		return emb_train


	def __matrix_m(self):

		X = self.emb_train[:,:-1]
		Y = self.emb_train[:,-1]

		# setting up LMNN
		lmnn = metric_learn.LMNN(k=self.metric_k, learn_rate=1e-2, verbose= True)

		# fit the data
		lmnn.fit(X, Y)

		# transform our input space
		X_lmnn = lmnn.transform()

		matrix_m = lmnn.metric()
		np.save('pickled_files/matrix_m_{}'.format(metric_k), matrix_m)

		self.__lmnn_knn(matrix_m)



	def __lmnn_knn(self, matrix_m):

		emb_test = self.embedding[60000:]

		predictions = dict()
		time_list = list()

		for k in range(1,k_test+1) : predictions[k] = list()

		start_time = time.time()
		for n, test_inst in enumerate(emb_test):

			## Calculate the distance of each test instance from train instances 
			eucl_dist_sorted = self.__eucl_dist_metric(test_inst[:-1], self.emb_train, matrix_m)

			for k in range(1,k_test+1):

				## Choose first k elements from sorted list 'temp_dist_idx'
				temp_first_k = eucl_dist_sorted[:k]
				temp_labels = [digit[1] for digit in temp_first_k]

				## Pick label that has majority count and append to prediction list
				temp_list = [temp_labels.count(i) for i in temp_labels]
				predictions[k].append(temp_labels[temp_list.index(max(temp_list))])

			time_list.append(round(time.time() - start_time))
			print(n,time_list[-1])
		
		path = "pickled_files/"
		with open(path + "predictions_knn_strong_metric" + '.pkl', 'wb') as f:
			pickle.dump(predictions, f, pickle.HIGHEST_PROTOCOL)


		return predictions
		


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

	

	def __eucl_dist_metric(self, instance, dataset, matrix_m):

		temp_inst = instance.reshape(1,-1)
		temp_inst = temp_inst.repeat(len(dataset), axis=0)
		difference = temp_inst - dataset[:,:-1]
		eucl_dist = np.diag(np.sqrt(np.matmul(np.matmul(difference, matrix_m),difference.T)))
		eucl_dist_sorted = [(eucl_dist[i], dataset[i,-1]) for i in range(len(dataset))]
		eucl_dist_sorted.sort()

		return eucl_dist_sorted 



def main():

	metric = Metric(relevant_idx_path, embedding, metric_k, k_test)


if __name__ == '__main__':

	relevant_idx_path = 'pickled_files/relevant_idx'
	embedding_path = 'pickled_files/embeddings.npy'
	embedding = np.load(embedding_path)
	metric_k = 40
	k_test = 100

	main()