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
outPath = "./output/6-open/"


fileList = [
    # "consolidation_1.jpg",
    # "consolidation_2.jpg",
    # "consolidation_4.jpg",
    # "consolidation_5.jpg",
    # "consolidation_6.jpg",
    # "consolidation_7.jpg",
    # "consolidation_8.jpg",
    # "consolidation_9.jpg",
    # "consolidation_10.jpg",
    # "consolidation_11.jpg",
    # "consolidation_12.jpg",
    "ground glass opacity_18.jpg",
    # "ground glass opacity_15.jpg",
    # "ground glass opacity_21.jpg",
    # "ground glass opacity_22.jpg",
    # "honeycombing_27.jpg",
    # "honeycombing_28.jpg",
    # "honeycombing_29.jpg",
    # "reticulation_42.jpg",
    # "reticulation_43.jpg",
    # "reticulation_44.jpg",
    # "reticulation_45.jpg",
    # "reticulation_46.jpg",
    # "reticulation_47.jpg",
    # "reticulation_48.jpg",
    "reticulation_50.jpg",
]



radiusList = [
    5, # 18
    38, # 50
]

margin = 100
for i in range(len(fileList)):
    i = len(fileList) - 1
    fileName = fileList[i]
    print("process filename " + fileName)
    radius = radiusList[i]
    img = cv2.imread(imgPath + fileName)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (radius, radius))
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    cv2.imwrite(outPath + fileName, img)
    break
