import os
import cv2
import numpy as np

groundTruthPath = "./visual/"
computeResultPath = "./consolidation/"

groundTruthList = os.listdir(groundTruthPath)
f = open('./similarity.txt', 'a')

for fileName in groundTruthList:
    truth_img = cv2.imread(groundTruthPath + fileName)
    result_img = cv2.imread(computeResultPath + fileName)
    height, width = truth_img.shape[0], truth_img.shape[1]
    f.write(fileName + '\n')

    both_count = 0
    count = 0
    truth_count = 0
    for r in range(height):
        for c in range(width):
            if all(truth_img[r, c] == (0, 255, 255)) and all(result_img[r, c] == (0, 255, 255)):
                both_count += 1
            if all(truth_img[r, c] == (0, 255, 255)) or all(result_img[r, c] == (0, 255, 255)):
                count += 1
            if all(truth_img[r, c] == (0, 255, 255)):
                truth_count += 1
    f.write('both ' + str(both_count) + '\n')
    f.write('count  ' + str(count) + '\n')
    
    print('both ' + str(both_count))
    print('count ' + str(count))
    print('truth_count ' + str(truth_count))
    # break