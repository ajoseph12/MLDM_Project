import os
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
    return abs(a-b)

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
                pattern_array = list(map(int, pattern.split(' #SUP:')[0].split(' ')[:-1]))
                distance = match_pattern(freeman_code_input, pattern_array)
                if distance != -1:
                    pattern_count += 1
                    relevance_criteria = distance/len(pattern_array)
                    relevance_criteria_count += relevance_criteria
        norm_rcc = relevance_criteria_count/pattern_count
        matches_array.append(norm_rcc)
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
                print('Now checking ' + str(code_count) + ' of ' + str(len_freem))
                fc_array = list(map(float, freeman_code.split(' ')))
                label = match_class(fc_array)
                if label == x:
                    positive_count += 1
        print('Accuracy for ' + str(x) + ': ' + str((positive_count/code_count)*100))

print(match_class([3, 3, 3, 3, 3, 4, 4, 3, 4, 4, 5, 4, 4, 5, 5, 5, 5, 5, 5, 5, 6, 6, 5, 7, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 3, 3, 5, 4, 4, 4, 4, 4, 7, 7, 0, 7, 0, 6, 6, 5, 5, 5, 4, 5, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 0, 0, 1, 0, 7, 0, 0, 7, 7, 0, 7, 1]))