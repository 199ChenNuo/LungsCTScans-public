import json
import cv2
import numpy as np
import math

jsonPath = "../instances_train2014.json"
imgPath = "../img/"
outputMaskPath = "./mask/"
outputImgPath = "./disease/"
highLightPath = "./visual/"
inputPath = "../parenchyma/traditional/output/result/"
resultPath = "./consolidation/"

image_list = []
categories = []
annotations = []

f = open('./similarity.txt', 'a')

def getContours(seg):
    contour = []
    for i in range(len(seg)):
        s = seg[i]
        contour.append([])
        for j in range(len(s) // 2):
            x = s[j * 2]
            y = s[j * 2 + 1]
            contour[i].append([[x, y]])
    return contour
        
def getPoint(i, s):
    l = len(s)
    return (int(s[(i * 2) % l]), int(s[(i * 2 + 1) % l]))

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

with open(jsonPath) as load_json:
    load_dict = json.load(load_json)
    image_list = load_dict['images']
    categories = load_dict['categories']
    annotations = load_dict['annotations']
    for i in range(len(image_list)):
        id = image_list[i]['id']
        box = annotations[i]['bbox']
        fileName = image_list[i]['file_name']
        segmentation = annotations[i]['segmentation']
        
        img = cv2.imread(imgPath + fileName)
        input_img = cv2.imread(inputPath + fileName)
        input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
        origin_input_img = cv2.imread(inputPath + fileName)
        origin_img = cv2.imread(imgPath + fileName)
        mask = np.zeros(img.shape, np.uint8)

        height, width = img.shape[0], img.shape[1]
        radius = 10
        r_block = math.ceil(height / radius)
        c_block = math.ceil(width / radius)

        # Get mask
        for j in range(len(segmentation)):
            s_len = len(segmentation[j])
            s = segmentation[j]
            for k in range(s_len // 2):
                p1 = getPoint(k, s)
                p2 = getPoint(k+1, s)
                cv2.line(mask, p1, p2, (255, 255, 255), 1, 4)
                cv2.line(origin_img, p1, p2, (0, 255, 255), 1, 4)
        
        # Fill in mask contour
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        contours,hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for index in range(len(contours)):
            cv2.fillPoly(mask, [contours[index]], 255)
        
        # find disease
        for r in range(r_block):
            for c in range(c_block):
                rate = histogram(input_img, r*radius, c*radius, radius)
                if rate>0.1:
                    end_idx = (r+1) * radius if (r+1) * radius < 512 else 512
                    cend_idx = (c+1) * radius if (c+1) * radius < 512 else 512
                    for i in range(r*radius, end_idx):
                        for j in range(c*radius, cend_idx):
                            if "consolidation" in fileName:
                                if input_img[i][j] >= 90 and input_img[i][j] <= 110:
                                    origin_input_img[i, j] = (0, 255, 255)
                            if "glass" in fileName:
                                if input_img[i][j] >= 40 and input_img[i][j] <= 80:
                                    origin_input_img[i, j] = (0, 255, 255)
                            if "honey" in fileName:
                                if input_img[i][j] >= 10 and input_img[i][j] <= 60:
                                    origin_input_img[i, j] = (0, 255, 255)
                            if "micro" in fileName:
                                if input_img[i][j] >= 50 and input_img[i][j] <= 90:
                                    origin_input_img[i, j] = (0, 255, 255)
                            if "reticulation" in fileName:
                                if input_img[i][j] >= 40 and input_img[i][j] <= 80:
                                    origin_input_img[i, j] = (0, 255, 255)
        
        truth_count = 0
        result_count = 0
        both_count = 0
        count = 0
        
        # cv2.imwrite(outputMaskPath + fileName, mask)
        height, width = img.shape[0], img.shape[1]
        for r in range(height):
            for c in range(width):
                if all(mask[r, c] == (0, 0, 0)):
                    img[r, c] = (0, 0, 0)
                else:
                    origin_img[r, c] = (0, 255, 255)
                    truth_count += 1
                if all(origin_input_img[r,c] == (0, 255, 255)):
                    result_count += 1
                if all(origin_input_img[r,c] == (0, 255, 255)) or all(origin_img[r,c] == (0, 255, 255)):
                    count += 1
                if all(origin_input_img[r,c] == (0, 255, 255)) and all(origin_img[r,c] == (0, 255, 255)):
                    both_count += 1
        
        print(fileName)
        print('both_count ' + str(both_count))
        print('count ' + str(count))
        print('truth_count ' + str(truth_count))
        print('result_count ' + str(result_count))
        print('\n')

        f.write(fileName + '\n')
        f.write('both_count ' + str(both_count) + '\n')
        f.write('count ' + str(count) + '\n')
        f.write('truth_count ' + str(truth_count) + '\n')
        f.write('result_count ' + str(result_count) + '\n')
        
    f.close()

        # cv2.imwrite(outputImgPath + fileName, disease)
        # cv2.imwrite(highLightPath + fileName, origin_img)


