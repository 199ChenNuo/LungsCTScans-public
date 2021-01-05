import cv2
import numpy as np
import os

# img = cv2.imread("../../img/honeycombing_23.jpg")
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ret1, th1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

# cv2.imwrite("./mask/honeycombing_23.jpg_mask.jpg", th1)
# print(ret1)

inputImgPath = "../../img/"
outputMaskPath = "./mask-OTSU/"

inputImgList = os.listdir(inputImgPath)
# print(inputImgList)

for fileName in inputImgList:
    img = cv2.imread(inputImgPath + fileName)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret1, th1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    cv2.imwrite(outputMaskPath + fileName + "_mask.jpg", th1)
