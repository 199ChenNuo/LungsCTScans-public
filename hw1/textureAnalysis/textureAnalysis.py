import os
import cv2
import math
from skimage.morphology import disk
import numpy as np
from skimage.feature import greycomatrix, greycoprops
from matplotlib import pyplot as plt

inputDir = "./disease/"
inputList = os.listdir(inputDir)

def CalMean(img, row, col, radius):
    mean = (0, 0, 0)
    count = 0
    # boundary condition
    row = img.shape[0] - radius if row + radius >= img.shape[0] else row
    col = img.shape[1] - radius if col + radius >= img.shape[1] else col

    for r in range(row, row + radius):
        for c in range(col, col + radius):
            if all(img[r, c] == (0, 0, 0)):
                continue
            else:
                print(img[r, c])
                mean += img[r, c]
                count += 1
    
    return mean / count if count != 0 else 0

def isSameValue(img, row, col, radius):
    mean = (0, 0, 0)
    count = 0
    # boundary condition
    row = img.shape[0] - radius if row + radius >= img.shape[0] else row
    col = img.shape[1] - radius if col + radius >= img.shape[1] else col

    for r in range(row, row + radius):
        for c in range(col, col + radius):
            if img[r, c][0] == img[r, c][1] and img[r, c][0] == img[r,c][2]:
                continue
            else:
                return False
    return True

def get_img(s): # s为图像路径
    values_temp = []
    input = cv2.imread(s, cv2.IMREAD_GRAYSCALE) # 读取图像，灰度模式 
    # 得到共生矩阵，参数：图像矩阵，距离，方向，灰度级别，是否对称，是否标准化
    # [0, np.pi / 4, np.pi / 2, np.pi * 3 / 4] 一共计算了四个方向，你也可以选择一个方向
    # 统计得到glcm
    glcm = greycomatrix(input, [2, 8, 16], [0, np.pi / 4, np.pi / 2, np.pi * 3 / 4], 256, symmetric=True, normed=True)  # , np.pi / 4, np.pi / 2, np.pi * 3 / 4
    print(glcm.shape) 
    # 循环计算表征纹理的参数 
    for prop in {'contrast', 'dissimilarity','homogeneity', 'energy', 'correlation', 'ASM'}:
        temp = greycoprops(glcm, prop)
        # temp=np.array(temp).reshape(-1)
        values_temp.append(temp)
        print("===================")
        print(prop, temp)
        print('len:',len(temp))
        print('')
    return (values_temp)

def histogram(grayfig, row, col, radius):
    row = img.shape[0] - radius if row + radius >= img.shape[0] else row
    col = img.shape[1] - radius if col + radius >= img.shape[1] else col
    ret = np.zeros(256)
    count = 0
    sum = 0
    for i in range(row, row+radius):
        for j in range(col, col+radius):
            if grayfig[i][j] == 0:
                continue
            ret[grayfig[i][j]] += 1
            count += 1
            sum += grayfig[i][j]
    if count == 0:
        return 0
    
    margin = 10
    gray_count = 0
    rate = 0.0
    mean = sum // count
    mean = 100
    for i in range(mean-margin, mean+margin):
        gray_count += ret[i]
    if count != 0:
        rate = gray_count / count
    # return ret
    return rate


count = 0
for fileName in inputList:
    print("process " + inputDir + fileName)

    img = cv2.imread(inputDir + fileName)
    img = cv2.erode(np.uint8(img), disk(5))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    height, width = img.shape[0], img.shape[1]
    radius = 50
    r_block = math.ceil(height / radius)
    c_block = math.ceil(width / radius)

    # 灰度共生矩阵
    # tmp = get_img(inputDir + fileName)

    # 灰度直方图
    max_rate = 0
    for r in range(r_block):
        for c in range(c_block):
            rate = histogram(img, r*radius, c*radius, radius)
            max_rate = max(max_rate, rate)
            # plt.plot(range(256), data)
            # plt.show()
            # cv2.waitKey(0)
    print(max_rate)
    # count += 1
    # if count == 10:
    #     break

