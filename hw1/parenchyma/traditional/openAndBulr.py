import cv2
import numpy as np
import os

inputImgPath =  "./mask-OTSU/"
outputImgPath = "./mask-open/"

inputImgList = os.listdir(inputImgPath)

for fileName in inputImgList:
    filePath = inputImgPath + fileName
    img = cv2.imread(filePath)

    height = img.shape[0]
    width = img.shape[1]
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5, 5))
    opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel,iterations=1)
    median = cv2.medianBlur(opened,5)
    cv2.imwrite(outputImgPath + fileName, median)


# img = cv2.imread(inputImgPath + "consolidation_1.jpg_mask.jpg")
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
# opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel,iterations=1)
# median = cv2.medianBlur(opened,5)
# cv2.imwrite(outputImgPath + "median.jpg", median)

# height = img.shape[0]
# width = img.shape[1]

# for r in range(height):
#     for c in range(width):
#         pixel = img[r, c]
#         img[r, c] = 255 - pixel
# closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
# cv2.imwrite(outputImgPath + "closed.jpg", closed)