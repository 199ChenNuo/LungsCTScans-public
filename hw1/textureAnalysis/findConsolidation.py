import cv2
import math
import numpy as np
from skimage.morphology import disk
import os

inputPath = "../parenchyma/traditional/output/result/"
inputList = os.listdir(inputPath)

# origin_img = cv2.erode(np.uint8(origin_img), disk(5))



def histogram(grayfig, row, col, radius):
    row = img.shape[0] - radius if row + radius >= img.shape[0] else row
    col = img.shape[1] - radius if col + radius >= img.shape[1] else col
    ret = np.zeros(256)
    count = 0
    sum = 0
    margin = 10
    mean = 100

    for i in range(row, row+radius):
        for j in range(col, col+radius):
            if grayfig[i][j] == 0:
                continue
            ret[grayfig[i][j]] += 1
            count += 1
            sum += grayfig[i][j]

    if count == 0:
        return 0
    
    gray_count = 0
    rate = 0.0
    # mean = sum // count
    for i in range(mean-margin, mean+margin):
        gray_count += ret[i]
    if count != 0:
        rate = gray_count / count
    # return ret
    return rate

for fileName in inputList:
    img = cv2.imread(inputPath + fileName)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    origin_img = cv2.imread(inputPath + fileName)

    height, width = img.shape[0], img.shape[1]
    radius = 10
    r_block = math.ceil(height / radius)
    c_block = math.ceil(width / radius)

    for r in range(r_block):
        for c in range(c_block):
            rate = histogram(img, r*radius, c*radius, radius)
            if (rate > 0.1):
                end_idx = (r+1) * radius if (r+1) * radius < 512 else 512
                cend_idx = (c+1) * radius if (c+1) * radius < 512 else 512
                for i in range(r*radius, end_idx):
                    for j in range(c*radius, cend_idx):
                        if img[i][j] >= 90 and img[i][j] <= 110:
                            origin_img[i,j] = (0, 255, 255)
                            # origin_img[i,j,2] = 1
    cv2.imwrite("./consolidation/" + fileName, origin_img)

# cv2.imwrite("./consolidation/" + str(radius) + "_consolidation_12.jpg", origin_img)


