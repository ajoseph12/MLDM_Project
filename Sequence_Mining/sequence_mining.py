import os
import ast
import numpy as np
import matplotlib.pyplot as plt
import glob
import random
"""
    the methods here are to:
    1) return most relevant matched class for a given freeman code
    2)visualize given pattern into an imag matrix
"""

def match_pattern(freeman_code_input, pattern):
    len_freeman_code_input = len(freeman_code_input)
    len_pattern = len(pattern)
    if len_freeman_code_input > len_pattern:
        distances_array = []
        for i in range(len_freeman_code_input - len_pattern):
            distance = 0
            for j in range(len_pattern):
                distance += _binary_distance(pattern[j], freeman_code_input[i + j])
            if distance == 0:
                return 0
            else:
                distances_array.append(distance)
        return min(distances_array)
    else:
        return -1

def _binary_distance(a, b):
    difference = abs(a-b)
    if difference > 4:
        return 8 - difference
    else:
        return difference
    

def _hamming_distance(a, b):
    return bin(a^b).count('1')

def match_class(freeman_code_input):
    pattern_dir = os.path.dirname(__file__)

    matches_array = []
    for x in range(10):
        pattern_count = 0
        relevance_criteria_count = 0
        with open(os.path.join(pattern_dir, "./filtered_patterns/" + str(x) + ".txt"), mode='r') as pattern_file:
            patterns = pattern_file.readlines()
            for pattern in patterns:
                pattern_array = ast.literal_eval(pattern)
                #print(pattern_array)
                distance = match_pattern(freeman_code_input, pattern_array)
                if distance != -1:
                    pattern_count += 1
                    relevance_criteria = distance/len(pattern_array)
                    relevance_criteria_count += relevance_criteria
        if pattern_count > 0:
            norm_rcc = relevance_criteria_count/pattern_count
            matches_array.append(norm_rcc)
        else:
            matches_array.append(1000000000)
    index_min = min(range(len(matches_array)), key=matches_array.__getitem__)
    return index_min

def acc_testing():
    for x in range(10):
        print('Starting for '+ str(x))
        code_count = 0
        positive_count = 0
        pattern_dir = os.path.dirname(__file__)
        with open(os.path.join(pattern_dir, "./input/input_patterns_for_" + str(x) + ".txt"), mode='r') as fc_code_file:
            freeman_codes = fc_code_file.readlines()
            len_freem = len(freeman_codes)
            for freeman_code in freeman_codes:
                code_count += 1
                if code_count%1000 == 0:
                    print('Now checking ' + str(code_count) + ' of ' + str(len_freem))
                fc_array = list(map(float, freeman_code.split(' ')[:-2 or None]))
                label = match_class(fc_array)
                if label == x:
                    positive_count += 1
        print('Accuracy for ' + str(x) + ': ' + str((positive_count/code_count)*100))

def get_visualized_patterns(digit):
    pattern_dir = os.path.dirname(__file__)
    mined_patterns = []
    with open(os.path.join(pattern_dir, "./filtered_patterns/" + str(digit) + ".txt"), mode='r') as pattern_file:
        patterns = pattern_file.readlines()
        for pattern in patterns:
            pattern_array = ast.literal_eval(pattern)
            mined_patterns.append(pattern_array)

    #randomly select  n patterns
    if len(mined_patterns) > 8:
        mined_patterns = random.sample(mined_patterns, 8)
    visualized = []
    files = glob.glob('static/images/seq_min_res/*')
    for f in files:
        os.remove(f)

    for index, mined_pattern in enumerate(mined_patterns):
        imgmatrix = get_image_matrix_from_freemancode(mined_pattern)
        plt.imshow(imgmatrix, cmap='binary', vmin=0, vmax=1)
        plt.axis('off')
        plt.savefig('static/images/seq_min_res/' + str(index) + '.png')
        visualized.append(mined_pattern)
    return visualized



def get_image_matrix_from_freemancode(freeman_code):
    img = np.zeros((40,40))

    x, y = 20, 20 
    img[y][x] = 1
    for direction in freeman_code:
        if direction in [1,2,3]:
            y -= 1
        if direction in [5,6,7]:
            y += 1
        if direction in  [3,4,5]:
            x -= 1
        if direction in [0,1,7]:
            x += 1

        img[y][x] = 1
    return img

#acc_testing()