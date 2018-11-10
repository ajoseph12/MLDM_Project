__author__ = 'rohil'

import mnist
import cv2
from PIL import Image
import numpy as np
from skimage import measure
import os
import pandas as pd


# def image_processing_for_freemancode(train=True, test=False):
#     images = []
#     if train:
#         images = mnist.train_images()
#         images_label = mnist.train_labels()
#     if test:
#         images = mnist.test_images()
#         images_label = mnist.test_labels()
#     array_with_freemancode = []
#     for i_no in range(images.shape[0]):
#         print('Processing image', i_no)
#         img_1 = images[i_no]
#
#         chain = basic_freeman_code_generator(img_1)
#
#         if train:
#             array_with_freemancode.append(['Train_image_' + str(i_no), np.array(chain)])
#         if test:
#             array_with_freemancode.append(['Test_Image_' + str(i_no), np.array(chain)])
#     print("Saving the results")
#     df1 = pd.DataFrame(columns=['Image_Label', 'Freeman_Code'])
#     for i in range(len(array_with_freemancode)):
#         df1.loc[i, 'Image_Label'] = array_with_freemancode[i][0]
#         df1.loc[i, 'Freeman_Code'] = array_with_freemancode[i][1]
#     return df1


def basic_freeman_code_generator(img_1):
    ret, img = cv2.threshold(img_1, 1, 255, 0)
    start_point = start_point_finder(img)

    directions = [0, 1, 2,
                  3, 4,
                  5, 6, 7]
    dir2idx = dict(zip(directions, range(len(directions))))
    change_i = [-1, -1, -1, 0, 1, 1, 1, 0]
    change_j = [-1, 0, 1, 1, 1, 0, -1, -1]
    border = []
    chain = []
    curr_point = start_point
    for direction in directions:
        idx = dir2idx[direction]
        new_point = (start_point[0] + change_i[idx], start_point[1] + change_j[idx])
        if img[new_point] != 0:  # if is ROI
            border.append(new_point)
            chain.append(direction)
            curr_point = new_point
            break

    count = 0

    while curr_point != start_point:
        # figure direction to start search
        b_direction = (chain[-1] + 5) % 8
        dirs_1 = range(b_direction, 8)
        dirs_2 = range(0, b_direction)
        dirs = []
        dirs.extend(dirs_1)
        dirs.extend(dirs_2)
        for direction in dirs:
            idx = dir2idx[direction]
            new_point = (curr_point[0] + change_i[idx], curr_point[1] + change_j[idx])
            if img[new_point] != 0:  # if is ROI
                border.append(new_point)
                chain.append(direction)
                curr_point = new_point
                break
        if count == 1000:
            break
        count += 1
    return chain, border, img


def start_point_finder(img):
    start_point = 0
    for i in np.arange(img.shape[0]):
        for j in np.arange(img.shape[1]):
            if i == 27 and j == 27:
                return start_point
            if img[i][j] > 0:
                start_point = (i, j)
                break
        else:
            continue
        break
    return start_point


def filter_noise(image, chain_border):
    df = pd.DataFrame(columns=['x_corr', 'y_corr'])
    for i in range(len(chain_border)):
        df.loc[i, 'x_corr'] = chain_border[i][0]
        df.loc[i, 'y_corr'] = chain_border[i][1]
    for idx, sub_group in df.groupby('x_corr'):
        image[int(idx), int(sub_group['y_corr'].min()):int(sub_group['y_corr'].max() + 1)] = 0
    return image


def regenerative_freemancode(image):
    chain_array = []
    image_array = [image]
    while True:
        start_point = start_point_finder(image_array[-1])
        if start_point == 0:
            break
        else:
            chain, image_filtered = iterative_removal_of_noise(image_array[-1])
            chain_array.append(chain)
            image_array.append(image_filtered)
    return chain_array, image_array


def iterative_removal_of_noise(image):
    chain, border, img = basic_freeman_code_generator(image)
    image_filtered = filter_noise(img, border)
    return chain, image_filtered


if __name__ == "__main__":
    # df = image_processing_for_freemancode(train=False, test=True)
    # df.to_hdf('/home/rohilrg/Documents/test.hdf', key='df', mode='w')

    images = mnist.train_images()
    display_image = images[47]
    print(type(display_image))
    for i in np.arange(display_image.shape[0]):
        for j in np.arange(display_image.shape[1]):
            if display_image[i][j] == 0:
                print(".", end="", flush=True)
            else:
                print("0", end="", flush=True)
        print()

    chain = regenerative_freemancode(display_image)
