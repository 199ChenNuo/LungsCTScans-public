from lungmask import mask
import SimpleITK as sitk
import os

# Use a trained network (not trained from this dataset)
# lungmask honeycombing_23.jpg honeycombing_23_output.jpg --noHU
filePath = "..\\..\\img\\"
inputFileList = os.listdir(filePath)
for f in inputFileList:
    com = "lungmask ..\\..\\img\\" + f + " .\\non-smooth\\mask\\" + f + "_output.jpg" + " --noHU"
    try:
        os.system(com)
    except:
        print("process " + f + " failed")


outputFilePath = "./hw1/output/"
outputs = os.listdir(outputFilePath)
print(outputs)