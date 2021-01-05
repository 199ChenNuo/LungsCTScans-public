import cv2
import os
import numpy as np

inputImgPath = "./mask-open/"
outputMaskPath = "./mask/"

inputImgList = os.listdir(inputImgPath)

for fileName in inputImgList:
    img = cv2.imread(inputImgPath + fileName)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contours,hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    area = []
    
    for index in range(len(contours)):
        area.append(cv2.contourArea(contours[index]))
    max_index = np.argmax(area)
    max_area = cv2.contourArea(contours[max_index])

    for index in range(len(contours)):
        if index != max_index:
            cv2.fillPoly(img, [contours[index]], 0)
    
    height = img.shape[0]
    width = img.shape[1]
    mask = np.zeros((height + 2, width + 2), np.uint8)
    cv2.floodFill(img, mask, (0, 0), 255)
    cv2.floodFill(img, mask, (height - 1, 0), 255)
    cv2.floodFill(img, mask, (height - 1, width - 1), 255)
    cv2.floodFill(img, mask, (0, width - 1), 255)

    for r in range(height):
        for c in range(width):
            img[r,c] = 255 - img[r, c]
    img = cv2.erode(img, np.ones([5, 5]))
    img = cv2.dilate(img, np.ones([5, 5]))
    # img = cv2.medianBlur(img, 5)
    cv2.imwrite(outputMaskPath + fileName, img)
