# import cv2 as cv
import os, os.path
from PIL import Image
from itertools import product
import math
from statistics import mean
import warnings

warnings.filterwarnings("ignore")  # Otherwise get warning due to size of images

pathTrain = "C:/Purdue/LeGrand/EOjpg/"  # Only have one file of imgs, will divide after
listFiles = os.listdir(pathTrain)

wChips = 18
hChips = 14
# wChips = 4
# hChips = 3
chipNames = []
for k in range(0, len(listFiles)):
    # for k in range(0, 1):
    img = Image.open(pathTrain + listFiles[k])

    w, h = img.size
    dW = math.floor(w / wChips)
    dH = math.floor(h / hChips)

    heightRange = range(0, h - h % dH, dH)
    widthRange = range(0, w - w % dW, dW)
    grid = product(heightRange, widthRange)
    for i, j in grid:
        # box = (j, i, j + dH, i + dW)
        box = (j, i, j + dW, i + dH)

        out = (
            "C:/Purdue/LeGrand/"  # Only one
            + "EOimgsChip/"
            + listFiles[k].rstrip(".jpg")
            + str(heightRange.index(i) + 1)
            + "_"
            + str(widthRange.index(j) + 1)
            # + str(i)
            # + str(j)
            + ".png"  # Or .tiff if want
        )
        chipName = str(k) + str(heightRange.index(i) + 1) + str(widthRange.index(j) + 1)
        chipNames.append(chipName)
        img.crop(box).save(out)
print("Part 1 Done")
for i in range(0, len(listFiles)):
    # for i in range(0, 1):
    img = Image.open(pathTrain + listFiles[i])
    w, h = img.size
    dW = math.floor(w / wChips)
    dH = math.floor(h / hChips)
    labelName = 0

    with open(
        "C:/Purdue/LeGrand/EOlabelsCorrected/"  # Only one folder
        + listFiles[i].rstrip(".jpg")
        + ".txt"
    ) as fo:
        lines = fo.readlines()
        # Image is divided into wChips * hChips, left -> right, top -> bottom. Attach bbox to corresponding chip as long as whole box fits in chip
        # Actually, for UNICORN this does not check whole bbox, just center of bbox
        for j in range(0, len(lines)):
            # for j in range(0, 1):
            if lines[j] == "\n":
                continue
            line = lines[j].split()
            line = [float(k) for k in line]
            # dW / w to normalize, bring from pixels to proportion
            caseX = math.ceil(line[1] / (dW / w))
            caseY = math.ceil(line[2] / (dH / h))
            # Chipped images use row by column, so here too
            labelName = listFiles[i].rstrip(".jpg") + str(caseY) + "_" + str(caseX)

            fileName = (
                "C:/Purdue/LeGrand/EOlabelsChip/" + labelName + ".txt"  # Only one file
            )

            label = lines[j].split()
            # Scale up width/height by depending on their number of chips
            label[3] = float(label[3]) * wChips
            label[4] = float(label[4]) * hChips
            # Scale x/y coords to be right proportion relative to new chips
            scaleX = 1 / wChips
            scaleY = 1 / hChips
            label[1] = (float(label[1]) % scaleX) / scaleX
            label[2] = (float(label[2]) % scaleY) / scaleY
            # Formatting
            label[0] = int(label[0])
            label = str(label) + "\n"
            label = label.replace(",", "").replace("[", "").replace("]", "")

            if os.path.isfile(fileName):
                with open(fileName, "a") as f:  # Append as new row to existing file
                    f.write(label)
            else:
                with open(fileName, "w") as f:  # Write new file
                    f.write(label)
