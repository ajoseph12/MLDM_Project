
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
from collections import Counter

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


def get_nearest_neighbours(train_samples, test_instance, matrix,average_matrix, k=1):
    train_samples.reset_index(drop=True,inplace=True)
    train_samples_1 = train_samples.copy()
    # Applying Triangle Inequality
    cost1, cost2, df_with_two_samples = provide_two_costs(test_instance, train_samples_1,average_matrix)
    train_samples_modified=0
    if cost1 == cost2:
        cost1, cost2, df_with_two_samples = provide_two_costs(test_instance, train_samples_1,average_matrix)
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
        s1 = ''.join(str(e) for e in s1)
        s2 = test_instance['Freeman Code']
        s2 = ''.join(str(e) for e in s2)
        #distance1 = mod_med_k(s1, s2,k=5)
        distance1 = distance(s1,s2)
        neighbour_information.loc[counter, 'Index_of_Train_Sample'] = idx
        neighbour_information.loc[counter, 'Distance'] = distance1
        neighbour_information.loc[counter, 'Label'] = label
        counter += 1
    neighbour_information.sort_values(by='Distance', inplace=True)

    if k < neighbour_information.shape[0]:
        k_nearest_neighbours = neighbour_information.iloc[:k]
    else:
        k_nearest_neighbours = neighbour_information.iloc[:(neighbour_information.shape[0])]
        k = neighbour_information.shape[0]
    counter = Counter(k_nearest_neighbours['Label'])
    if len(counter) > 1:
        first_prediction = counter.most_common()[0][0]
        number_of_neighbours_in_favour_first_predictions = counter.most_common()[0][1]

        second_prediction = counter.most_common()[1][0]
        number_of_neighbours_in_favour_second_predictions = counter.most_common()[1][1]

        probablity_class_of_first_prediction = float(number_of_neighbours_in_favour_first_predictions)/k
        probablity_class_of_second_prediction = float(number_of_neighbours_in_favour_second_predictions)/k

        return first_prediction, second_prediction, probablity_class_of_first_prediction\
               ,probablity_class_of_second_prediction,  k_nearest_neighbours
    else:
        first_prediction = counter.most_common()[0][0]
        number_of_neighbours_in_favour_first_predictions = counter.most_common()[0][1]

        probablity_class_of_first_prediction = float(number_of_neighbours_in_favour_first_predictions) / k

        return first_prediction, None, probablity_class_of_first_prediction, None, k_nearest_neighbours

def calculate_accuracy_of_model(train_samples, test_instances, matrix,average_matrix, k=1):
    label = list()
    for idx, test_instance in test_instances.iterrows():
        print('The test instance calculated now is:',idx)
        lb1,lb2,pb1,pb2,_=get_nearest_neighbours(train_samples,test_instance,matrix,average_matrix,k=k)
        label.append(lb1)
        print('The first predictied label is',lb1,'with class probability of',pb1)
        print('The second predictied label is', lb2, 'with class probability of', pb2)
    label = np.ravel(label).astype(int)
    true_label=np.ravel(np.array(test_instances['Label'].astype(int)))
    accuracy = accuracy_score(true_label,label)
    print()
    return accuracy
def removal_of_unnecessary_examples(cost1, cost2, df_with_two_samples, matrix, train_samples_1, j= None):
    index = int(df_with_two_samples.index[j])
    label = df_with_two_samples['Label'].values[j]
    radius_of_the_inner_sphere = abs(cost1 - cost2)
    radius_of_the_outer_sphere = abs(cost1 + cost2)

    array = matrix[index, :]
    idx = 0
    for i in np.nditer(array):
        if i <= radius_of_the_inner_sphere or i >= radius_of_the_outer_sphere:
            #train_samples_1.drop(train_samples_1.index[idx], axis=0, inplace=True)
            train_samples_1 = train_samples_1[train_samples_1.index != idx]
        idx += 1

    train_samples_2 = train_samples_1[train_samples_1['Label'] != label]
    print('The training samples got reduced to', train_samples_2.shape[0])
    return train_samples_2

def generation_of_average_matrix(train_samples,matrix):
    average_matrix = np.zeros((10,10))
    train_samples.reset_index(drop=True, inplace=True)
    for i in itertools.combinations(enumerate(np.array([0,1,2,3,4,5,6,7,8,9])),2):
        ts1 = train_samples[train_samples['Label'].astype(int)==i[0][1]]
        ts2 = train_samples[train_samples['Label'].astype(int)==i[1][1]]
        indexes_ts1 = ts1.index
        indexes_ts2 = ts2.index
        no_of_index_to_choose = min(len(indexes_ts1),len(indexes_ts2))
        if no_of_index_to_choose == len(indexes_ts1):
            indexes_ts2 = np.random.choice(indexes_ts2,no_of_index_to_choose)
        if no_of_index_to_choose == len(indexes_ts2):
            indexes_ts1 = np.random.choice(indexes_ts1,no_of_index_to_choose)
        avg= np.average(np.ravel(matrix[indexes_ts1,indexes_ts2]))

        average_matrix[i[0][0],i[1][0]] = avg
    for i in range(len(average_matrix)):
        for j in range(len(average_matrix)):
            average_matrix[j,i] = average_matrix[i,j]
    return average_matrix


def provide_two_costs(test_instance, train_samples, average_matrix):


    ## Trying to select the best example from Training Sample

    length_of_the_test_set = len(test_instance['Freeman Code'])

    new_df = train_samples[((length_of_the_test_set-1)<train_samples['Length'])
                           &(train_samples['Length'] <(length_of_the_test_set+1))]
    new_df_copy = new_df.copy()

    for idx, train_sample in new_df_copy.iterrows():
        s1 = train_sample['Freeman Code']
        s1 = ''.join(str(e) for e in s1)
        s2 = test_instance['Freeman Code']
        s2 = ''.join(str(e) for e in s2)
        # distance1 = mod_med_k(s1, s2,k=5)
        distance1 = distance(s1, s2)
        new_df_copy.loc[idx, 'Distance_with_test_label'] = distance1

    first_example_selected = new_df_copy[
        new_df_copy['Distance_with_test_label'] == new_df_copy['Distance_with_test_label'].min()]
    if len(first_example_selected)>1:
        first_example_selected = first_example_selected.iloc[[0]]
    cost1 = first_example_selected['Distance_with_test_label'].values
    cost1 = float(cost1[0])
    #cost1 = modified_med(np.ravel(first_example_selected['Freeman Code'])[0], test_instance['Freeman Code'])
    first_example_selected = first_example_selected.drop('Distance_with_test_label', axis=1)
#######################################################################################################################

    label_first_example = int(first_example_selected['Label'])
    array_of_label = np.ravel(average_matrix[label_first_example, :])
    value_index_to_go = np.argsort(array_of_label,axis=0)[1]

    next_label_to_be_chosen = np.argmax(np.ravel(average_matrix[value_index_to_go,:]),axis=0)
    next_label_df = train_samples[train_samples['Label'] == float(next_label_to_be_chosen)]

    next_label_df_copy = next_label_df.copy()
    for idx, train_sample in next_label_df.iterrows():
        s1 = train_sample['Freeman Code']
        s1 = ''.join(str(e) for e in s1)
        s2 = test_instance['Freeman Code']
        s2 = ''.join(str(e) for e in s2)
        # distance1 = mod_med_k(s1, s2,k=5)
        distance1 = distance(s1, s2)
        next_label_df_copy.loc[idx, 'Distance_with_test_label'] = distance1
    second_example_selected = next_label_df_copy[
        next_label_df_copy['Distance_with_test_label'] == next_label_df_copy['Distance_with_test_label'].max()]
    cost2 = second_example_selected['Distance_with_test_label'].values
    cost2 = float(cost2[0])
    second_example_selected = second_example_selected.drop('Distance_with_test_label', axis=1)

    df_with_two_samples = pd.concat([first_example_selected,second_example_selected],axis=0)
    print(cost1,cost2)
    return cost1, cost2, df_with_two_samples


if __name__ == "__main__":
    # train = np.load('/home/rohilrg/Documents/MLDM Project Data Files/train_test_final/train_X.npy')
    # test = np.load('/home/rohilrg/Documents/MLDM Project Data Files/train_test_final/test_X.npy')
    # d = train[:1000]
    # g = test
    train_hdf = pd.read_hdf('/home/rohilrg/Documents/MLDM Project Data Files/train_freemancode_modified.hdf')
    # train_hdf = train_hdf.iloc[:2000]
    average_matrix = np.load('/home/rohilrg/Documents/MLDM Project Data Files/average_matrix.npy')
    test_instance = pd.read_hdf('/home/rohilrg/Documents/MLDM Project Data Files/train_test_final/test_freemancode.hdf')
    test_instance = test_instance.iloc[6205:6300]

    matrix = np.load('/home/rohilrg/Downloads/matrix_with_edit_distance_modified.npy')
    start = timeit.default_timer()
    #avg_matrix = generation_of_average_matrix(train_hdf, matrix)
    #np.save('/home/rohilrg/Documents/MLDM Project Data Files/average_matrix.npy',avg_matrix)
    k = calculate_accuracy_of_model(train_hdf,test_instance,matrix,average_matrix, k=20)
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