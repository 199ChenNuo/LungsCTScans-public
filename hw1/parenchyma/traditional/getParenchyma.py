import os
import cv2

inputImgPath = "../../img/"
maskPath = "./output/mask/"
outputPath = "./output/result/"

inputImgList = os.listdir(inputImgPath)

for fileName  in inputImgList:
    img = cv2.imread(inputImgPath + fileName)
    mask = cv2.imread(maskPath + fileName)
    mask = cv2.medianBlur(mask, 5)
    height, width = img.shape[0], img.shape[1]

    for r in range(height):
        for c in range(width):
            if all(mask[r, c] == (0, 0, 0)):
                img[r, c] = (0, 0, 0)
    
    cv2.imwrite(outputPath + fileName, img)
