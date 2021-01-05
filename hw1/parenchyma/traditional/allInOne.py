import cv2
import os
import numpy as np
from skimage.morphology import disk

inputPath = "../../img/"
outputPath = "./output/"

inputImgList = os.listdir(inputPath)

def getMask(imgName):
    # devide frontground and background
    img = cv2.imread(inputPath + imgName)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret1, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    cv2.imwrite(outputPath + "1-OTSU/" + imgName, mask)

    # remove noise
    height, width = img.shape[0], img.shape[1]
    mask = cv2.bitwise_not(mask)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.bitwise_not(mask)
    cv2.imwrite(outputPath + "2-morph/" + imgName, mask)

    # get the biggest area
    contours,hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    area = []
    for index in range(len(contours)):
        area.append(cv2.contourArea(contours[index]))
    max_index = np.argmax(area)
    max_area = cv2.contourArea(contours[max_index])
    for index in range(len(contours)):
        if index != max_index:
            cv2.fillPoly(mask, [contours[index]], 0)
    height = mask.shape[0]
    width = mask.shape[1]
    maskKernel = np.zeros((height + 2, width + 2), np.uint8)
    cv2.floodFill(mask, maskKernel, (0, 0), 255)
    cv2.floodFill(mask, maskKernel, (height - 1, 0), 255)
    cv2.floodFill(mask, maskKernel, (height - 1, width - 1), 255)
    cv2.floodFill(mask, maskKernel, (0, width - 1), 255)
    cv2.imwrite(outputPath + "3-fillhole/" + imgName, mask)

    # remove small area
    mask = cv2.bitwise_not(mask)
    mask = cv2.erode(np.uint8(mask), disk(5))
    contours,hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    areaSize = []
    for index in range(len(contours)):
        areaSize.append(cv2.contourArea(contours[index]))
        if areaSize[index] < 1200:
            cv2.fillPoly(mask, [contours[index]], 0)
    mask = cv2.dilate(np.uint8(mask), disk(5))
    cv2.imwrite(outputPath +"4-remove/" + imgName, mask)

    # get final result
    for r in range(height):
        for c in range(width):
            if all(mask[r, c] == (0, 0, 0)):
                img[r, c] = (0, 0, 0)
    cv2.imwrite(outputPath + "result/" + imgName, img)

for filename in inputImgList:
    getMask(filename)

# img = cv2.imread(inputImg)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ret1, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

# height, width = img.shape[0], img.shape[1]

# mask = cv2.bitwise_not(mask)
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))


# mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
# mask = cv2.bitwise_not(mask)

# contours,hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# area = []

# for index in range(len(contours)):
#     area.append(cv2.contourArea(contours[index]))
# max_index = np.argmax(area)
# max_area = cv2.contourArea(contours[max_index])

# for index in range(len(contours)):
#     if index != max_index:
#         cv2.fillPoly(mask, [contours[index]], 0)

# height = mask.shape[0]
# width = mask.shape[1]
# maskKernel = np.zeros((height + 2, width + 2), np.uint8)
# cv2.floodFill(mask, maskKernel, (0, 0), 255)
# cv2.floodFill(mask, maskKernel, (height - 1, 0), 255)
# cv2.floodFill(mask, maskKernel, (height - 1, width - 1), 255)
# cv2.floodFill(mask, maskKernel, (0, width - 1), 255)


# mask = cv2.bitwise_not(mask)

# contours,hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# areaSize = []

# for index in range(len(contours)):
#     areaSize.append(cv2.contourArea(contours[index]))
#     if areaSize[index] < 1000:
#         cv2.fillPoly(mask, [contours[index]], 0)


# for r in range(height):
#     for c in range(width):
#         if all(mask[r, c] == (0, 0, 0)):
#             img[r, c] = (0, 0, 0)
