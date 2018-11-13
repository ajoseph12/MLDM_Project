__author__ = 'rohil'

import numpy as np
from tool_for_freeman_code_gen import basic_freeman_code_generator, regenerative_freemancode
from Modified_Edit_Distance import modified_med, mod_med_k
import itertools
import timeit
import multiprocessing
import pandas as pd


def generate_freemancode_dataset(dataset):
    df_array = []
    print('Generating Freemancodes')
    for i in range(dataset.shape[0]):
        print('Processing image:', i + 1, 'and total images left are:', dataset.shape[0] - (i + 1))
        image = dataset[i][0]
        freemancode = regenerative_freemancode(image)
        df_array.append([np.array(freemancode)])
    df_array = np.array(df_array)
    print('Finishing Freemancodes')
    return df_array


def edit_distance_matrix_gen(dataset):
    # Generate a zero matrix of shape N*N
    matrix = np.zeros((dataset.shape[0], dataset.shape[0]))
    counter = 0
    for combi in itertools.combinations(enumerate(dataset), 2):
        # Generate the freemancode for both images
        # freemancode1 = basic_freeman_code_generator(combi[0][1][0])
        # freemancode2 = basic_freeman_code_generator(combi[1][1][0])

        # Generate the cost of the two freemancode
        cost, __ = mod_med_k(combi[0][1][0], combi[1][1][0])

        # Save the cost in the corrsponding cell of the matrix
        matrix[combi[0][0], combi[1][0]] = cost
        counter += 1
    return matrix


if __name__ == "__main__":
    train = np.load('/home/rohilrg/Documents/MLDM Project Data Files/Data_zip/train_X.npy')
    d = train[30000:60000]
    start = timeit.default_timer()
    df = generate_freemancode_dataset(d)
    np.save('/home/rohilrg/Documents/MLDM Project Data Files/array_with_freemancodes_test.npy', df)
    # dataset = np.load('/home/rohilrg/Documents/MLDM Project Data Files/array_with_freemancodes.npy')
    # dataset = dataset[:300]
    # matrix = edit_distance_matrix_gen(dataset)
    # np.save('/home/rohilrg/Documents/MLDM Project Data Files/matrix_with_edit_distance.npy', matrix)
    stop = timeit.default_timer()
    print('Time: ', stop - start)
# pool = multiprocessing.Pool(processes=2)
# freemancode1, __ = pool.map(basic_freeman_code_generator, combi[0][1][0])
# P2 = process(target=basic_freeman_code_generator, args=(combi[1][1][0],))
# freemancode2, __ = pool.map(basic_freeman_code_generator, combi[1][1][0])
