__author__ = 'rohil'

import mnist
import cv2
from PIL import Image
import numpy as np
from skimage import measure
import os
import pandas as pd



def image_processing_for_freemancode(train= True,test=False):
    images=[]
    if train:
        images= mnist.train_images()
        images_label = mnist.train_labels()
    if test:
        images = mnist.test_images()
        images_label = mnist.test_labels()
    array_with_freemancode=[]
    for i_no in range(images.shape[0]):
        print('Processing image',i_no)
        img_1= images[i_no]

        ret, img = cv2.threshold(img_1, 70, 255, 0)
        start_point=0
        for i, row in enumerate(img):
            for j, value in enumerate(row):
                if value == 255:
                    start_point = (i, j)

                    break
            else:
                continue
            break

        directions = [0, 1, 2,
                      7,     3,
                      6, 5, 4]
        dir2idx = dict(zip(directions, range(len(directions))))

        change_j = [-1, 0, 1,  # x or columns
                    -1, 1,
                    -1, 0, 1]

        change_i = [-1, -1, -1,  # y or rows
                    0, 0,
                    1, 1, 1]

        border = []
        chain = []
        curr_point = start_point
        for direction in directions:
            idx = dir2idx[direction]
            new_point = (start_point[0] + change_i[idx], start_point[1] + change_j[idx])
            if new_point[0]<28 and new_point[1]<28:
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

                if new_point[0]<28 and new_point[1]<28:
                    if img_1[new_point] != 0:  # if is ROI
                        border.append(new_point)
                        chain.append(direction)
                        curr_point = new_point
                        break
            if count == 1000: break
            count += 1


        if train:
            array_with_freemancode.append(['Train_image_'+str(i_no),np.array(chain)])
        if test:
            array_with_freemancode.append(['Test_Image_'+str(i_no),np.array(chain)])
    print("Saving the results")
    df1 = pd.DataFrame(columns=['Image_Label', 'Freeman_Code'])
    for i in range(len(array_with_freemancode)):
        df1.loc[i, 'Image_Label'] = array_with_freemancode[i][0]
        df1.loc[i, 'Freeman_Code'] = array_with_freemancode[i][1]
    return df1


if __name__ == "__main__":
  df = image_processing_for_freemancode(train=True,test=False)
  df.to_hdf('/home/rohilrg/Documents/test.hdf',key='df',mode='w')