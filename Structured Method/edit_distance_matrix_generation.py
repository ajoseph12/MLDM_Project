__author__ = 'rohil'

import numpy as np
from tool_for_freeman_code_gen import basic_freeman_code_generator
from Modified_Edit_Distance import modified_med
import itertools


def edit_distance_matrix_gen(dataset):
    matrix = np.zeros((dataset.shape[0], dataset.shape[0]))
    for combi in itertools.combinations(enumerate(dataset), 2):
        freemancode1, __ = basic_freeman_code_generator(combi[0][1][0])
        freemancode2, __ = basic_freeman_code_generator(combi[1][1][0])
        cost, __ = modified_med(freemancode1, freemancode2)
        print(cost)
        matrix[combi[0][0], combi[1][0]] = cost
    return matrix


if __name__ == "__main__":
    train = np.load('/home/rohilrg/Documents/MLDM Project Data Files/Data_zip/train_X.npy')
    d = train[:10]
    matrix = edit_distance_matrix_gen(d)
    print(matrix)
