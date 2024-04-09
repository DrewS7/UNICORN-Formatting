# import cv2 as cv
import os, os.path
from PIL import Image
from itertools import product
import math
import shutil

# This script takes only the labels which correspond to the images I have
pathImg = "C:/Purdue/LeGrand/EOjpg/"
pathLabel = "C:/Purdue/LeGrand/EOlabels/"
listImgs = os.listdir(pathImg)
listLabels = os.listdir(pathLabel)
kStore = []
for i in range(0, len(listImgs)):
    # for i in range(0, 2):
    for k in range(0, len(listLabels)):
        imgName = listImgs[i]
        imgName = imgName.lstrip("NITFVIS")
        imgName = imgName.rstrip(".jpg")
        labelName = listLabels[k]
        labelName = labelName.lstrip("NITFVIS")
        labelName = labelName.rstrip(".txt")
        if imgName == labelName:
            kStore.append(k)
for k in kStore:
    shutil.copyfile(
        "C:/Purdue/LeGrand/EOlabels/" + listLabels[k],
        "C:/Purdue/LeGrand/EOlabelsOnlyForImgs/" + listLabels[k],
    )
