import numpy as np
import os
import matplotlib.pyplot as plt
from skimage.morphology import disk, remove_small_objects
from scipy.ndimage import binary_fill_holes
from skimage.measure import label
from skimage import morphology, measure
import cv2
from cv2 import dilate, erode, bitwise_not
from PIL import Image
 
def maxminscale(tmp):
	if (len(np.unique(tmp)) > 1):
		tmp = tmp - np.amin(tmp)
		tmp = 255/np.amax(tmp)*tmp
	return tmp

imgPath = "./output/4-remove/"
outPath = "./output/5-close/"


fileList = [
    "consolidation_1.jpg",
    "consolidation_2.jpg",
    "consolidation_4.jpg",
    "consolidation_5.jpg",
    "consolidation_6.jpg",
    "consolidation_7.jpg",
    "consolidation_8.jpg",
    "consolidation_9.jpg",
    "consolidation_10.jpg",
    "consolidation_10.jpg",
    "consolidation_11.jpg",
    "consolidation_12.jpg",
    "ground glass opacity_14.jpg",
    "ground glass opacity_15.jpg",
    "ground glass opacity_21.jpg",
    "ground glass opacity_22.jpg",
    "honeycombing_27.jpg",
    "honeycombing_28.jpg",
    "honeycombing_29.jpg",
    "reticulation_42.jpg",
    "reticulation_43.jpg",
    "reticulation_44.jpg",
    "reticulation_45.jpg",
    "reticulation_46.jpg",
    "reticulation_47.jpg",
    "reticulation_48.jpg",
    "reticulation_49.jpg",
]



radiusList = [
    7, # 1
    7, # 2
    12, # 4
    20, # 5
    50, # 6
    70, # 7
    70, # 8
    60, # 9
    120, # 10
    40, # 10 iterate 2 times
    50, # 11
    90, # 12
    3, # groud glass 14
    10, # 15
    7, # 21
    3, # 22
    7, # 27
    7, # 28
    5, # 29
    3, # 42
    5, # 43
    3, # 44
    5, # 45
    15, # 46
    19, # 47
    25, # 48
    10
]

fileName = "consolidation_5.jpg"
margin = 100
for i in range(len(fileList)):
    i = len(fileList) - 1
    fileName = fileList[i]
    print("process filename " + fileName)
    radius = radiusList[i]
    img = cv2.imread(imgPath + fileName)
    img = cv2.copyMakeBorder(img, margin, margin, margin, margin, cv2.BORDER_CONSTANT, value=[0,0,0])
    img = remove_small_objects(label(img).astype(bool), min_size=1000)
    
    labels = label(img)

    mask = np.zeros(img.shape)
    # mask = np.zeros((img.shape[0] + 200, img.shape[1] + 200))
    for i in range(1, len(np.unique(labels))):
        tmp = np.zeros(labels.shape)
        tmp[labels == i] = 1
        curmask = dilate(np.uint8(tmp), disk(radius)) # 17 : radius of 2D-disk
        curmask = remove_small_objects(label(bitwise_not(maxminscale(curmask))).astype(bool), min_size = 500).astype(int)
        curmask[curmask != 0] = -1
        curmask = np.add(curmask, np.ones(curmask.shape))
        filled_tmp = erode(np.uint8(curmask), disk(radius))
        mask += filled_tmp
    
    # di = cv2.dilate(np.uint8(mask), disk(radius))
    # er = cv2.erode(np.uint8(di), disk(radius))
    # mask = cv2.bitwise_not(mask)
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
    # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # mask = cv2.bitwise_not(mask)

    mask = mask[margin:margin + 512, margin:margin + 512]
    print("write " + fileName)
    cv2.imwrite(outPath + fileName, mask * 255)

    break
