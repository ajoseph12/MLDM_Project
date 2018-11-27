
__author__ = 'rohil'

import numpy as np
from tool_for_freeman_code_gen import basic_freeman_code_generator, regenerative_freemancode
from Modified_Edit_Distance import modified_med, mod_med_k
import itertools
import timeit
import pandas as pd
from progressbar import *
from scipy.stats import mode
from Levenshtein import jaro_winkler, distance
from sklearn.metrics import accuracy_score


def generate_freemancode_dataset(dataset):
    df_array = []
    print('Generating Freemancodes')

    for i in range(dataset.shape[0]):

        print('Processing image:', i + 1, 'and total images left are:', dataset.shape[0] - (i + 1))
        if len(dataset) == 1:
            image = dataset[0]
        else:
            image = dataset[i][0]
        freemancode = regenerative_freemancode(image)
        df_array.append([np.array(freemancode)])
    df_array = np.array(df_array)
    print('Finishing Freemancodes')
    return df_array


def edit_distance_matrix_gen(dataset):
    # Generate a zero matrix of shape N*N
    matrix = np.zeros((dataset.shape[0], dataset.shape[0]))

    dataset_freemancode = dataset['Freeman Code']

    for combi in itertools.combinations(enumerate(dataset_freemancode), 2):

        # Generate the freemancode for both images
        # freemancode1 = basic_freeman_code_generator(combi[0][1][0])
        # freemancode2 = basic_freeman_code_generator(combi[1][1][0])
        if combi[1][0] == 5096:
            print('The row', combi[0][0]+1, 'row completed', 5095-combi[0][0])
        # Generate the cost of the two freemancode
        cost= modified_med(combi[0][1], combi[1][1])

        # Save the cost in the corrsponding cell of the matrix
        matrix[combi[0][0], combi[1][0]] = cost

        if (combi[0][0]==100 and combi[1][0] == 5096) or (combi[0][0]==200 and combi[1][0] == 5096) or (combi[0][0]==500 and combi[1][0] == 5096) or (combi[0][0]==1000 and combi[1][0] == 5096) or (combi[0][0]==3000 and combi[1][0] == 5096) or (combi[0][0]== 5000 and combi[1][0] == 5096):
            print('saving intermediate matrix')
            np.save(('/home/student/Project_Files/matrix_with_edit_distance{}.npy'.format(combi[0][0])), matrix)

    return matrix


def get_nearest_neighbours(train_samples, test_instance, matrix, k=1):
    train_samples.reset_index(drop=True,inplace=True)
    train_samples_1 = train_samples.copy()
    # Applying Triangle Inequality
    cost1, cost2, df_with_two_samples = provide_two_costs(test_instance, train_samples_1)
    train_samples_modified=0
    if cost1 == cost2:
        cost1, cost2, df_with_two_samples = provide_two_costs(test_instance, train_samples_1)
    if cost1 > cost2:
        train_samples_modified = removal_of_unnecessary_examples(cost1, cost2, df_with_two_samples, matrix, train_samples_1,
                                                          j=0)
    if cost1 < cost2:
        train_samples_modified = removal_of_unnecessary_examples(cost1, cost2, df_with_two_samples, matrix, train_samples_1,
                                                          j=1)

    # Now calculate the cost for remaining examples

    neighbour_information = pd.DataFrame(
        columns=['Index_of_Train_Sample','Distance', 'Label'])
    counter = 0
    for idx, train_sample in train_samples_modified.iterrows():
        s1 = train_sample['Freeman Code']
        label = train_sample['Label']
        #s1 = ''.join(str(e) for e in s1)
        s2 = test_instance['Freeman Code']
        #s2 = ''.join(str(e) for e in s2)
        distance1 = mod_med_k(s1, s2,k=1)
        #distance1 = distance(s1,s2)
        neighbour_information.loc[counter, 'Index_of_Train_Sample'] = idx
        neighbour_information.loc[counter, 'Distance'] = distance1
        neighbour_information.loc[counter, 'Label'] = label
        counter += 1
    neighbour_information.sort_values(by='Distance', inplace=True)

    k_nearest_neighbours = neighbour_information.iloc[:k]

    array_with_prediction = mode(k_nearest_neighbours['Label'], axis=0)

    prediction_label = array_with_prediction[0]
    number_of_neighbours_in_favour = array_with_prediction[1]

    return prediction_label, number_of_neighbours_in_favour, k_nearest_neighbours
def calculate_accuracy_of_model(train_samples, test_instances, matrix, k=1):
    label = list()
    for idx, test_instance in test_instances.iterrows():
        print(idx)
        lb,_,_=get_nearest_neighbours(train_samples,test_instance,matrix,k=k)
        label.append(lb)
    label = np.ravel(label).astype(int)
    true_label=np.ravel(np.array(test_instances['Label'].astype(int)))
    accuracy = accuracy_score(true_label,label)

    return accuracy
def removal_of_unnecessary_examples(cost1, cost2, df_with_two_samples, matrix, train_samples_1, j=None):
    index = int(df_with_two_samples.index[j])
    radius_of_the_inner_sphere = abs(cost1 - cost2)
    radius_of_the_outer_sphere = abs(cost1 + cost2)

    array = matrix[index, :]
    idx = 0
    for i in np.nditer(array):
        if i <= radius_of_the_inner_sphere or i >= radius_of_the_outer_sphere:
            #train_samples_1.drop(train_samples_1.index[idx], axis=0, inplace=True)
            train_samples_1 = train_samples_1[train_samples_1.index != idx]
        idx += 1
    return train_samples_1


def provide_two_costs(test_instance, train_samples):
    df_with_two_samples = train_samples.sample(n=2, axis=0)
    indexes = df_with_two_samples.index
    cost1 = modified_med(df_with_two_samples.loc[indexes[0], 'Freeman Code'], test_instance['Freeman Code'])
    cost2 = modified_med(df_with_two_samples.loc[indexes[1], 'Freeman Code'], test_instance['Freeman Code'])
    return cost1, cost2, df_with_two_samples


if __name__ == "__main__":
    # train = np.load('/home/rohilrg/Documents/MLDM Project Data Files/train_test_final/train_X.npy')
    # test = np.load('/home/rohilrg/Documents/MLDM Project Data Files/train_test_final/test_X.npy')
    # d = train[:1000]
    # g = test
    train_hdf = pd.read_hdf('/home/rohilrg/Documents/MLDM Project Data Files/train_freemancode_modified.hdf')
    # train_hdf = train_hdf.iloc[:2000]

    test_instance = pd.read_hdf('/home/rohilrg/Documents/MLDM Project Data Files/test_freemancode.hdf')
    test_instance = test_instance.iloc[9188:9198]

    matrix = np.load('/home/rohilrg/Downloads/matrix_with_edit_distance_modified.npy')
    start = timeit.default_timer()

    k = calculate_accuracy_of_model(train_hdf,test_instance,matrix, k=5)
    print(k)
    # cost_list = get_nearest_neighbours(train_hdf, train_hdf, test_instance)
    # df = generate_freemancode_dataset(d)
    # print(df)
    # df1 = generate_freemancode_dataset(g)
    # np.save('/home/rohilrg/Documents/MLDM Project Data Files/train_freeman_code.npy', df)
    # np.save('/home/rohilrg/Documents/MLDM Project Data Files/test_freeman_code.npy', df1)
    #matrix = np.load('/home/rohilrg/Downloads/matrix_with_edit_distance_modified.npy')
    #dataset = dataset.iloc[:100]

    #matrix = edit_distance_matrix_gen(dataset)
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    #np.save('/home/student/Project_Files/matrix_with_edit_distance.npy', matrix)
# pool = multiprocessing.Pool(processes=2)
# freemancode1, __ = pool.map(basic_freeman_code_generator, combi[0][1][0])
# P2 = process(target=basic_freeman_code_generator, args=(combi[1][1][0],))
# freemancode2, __ = pool.map(basic_freeman_code_generator, combi[1][1][0])