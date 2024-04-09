from osgeo import gdal
import pandas as pd

# import matplotlib.pyplot as plt
# import cv2 as cv
import os, os.path
from osgeo import ogr, osr

# import subprocess
import sys

# print(sys.version)
# print(sys.executable)

from pyproj import Proj


listFiles = os.listdir("C:/Purdue/LeGrand/EO")
numFiles = len(listFiles)

df = pd.read_csv("C:/Purdue/LeGrand/wamitt_gotcha_csv.csv")
imgIDs = df["track_point.fileId"]  # Pandas series of fileId column
classesPd = df["target_type.name"]
boxWidth = df["track.width"]
boxLength = df["track.length"]
trackLat = df["track_point.latitude"]
xCenter = df["track_point.x"]
yCenter = df["track_point.y"]
trackLong = df["track_point.longitude"]

# print(imgIDs.value_counts()["NITFVIS2008081614414001004700"])
# exit()
trackIDsList = imgIDs.tolist()  # Pandas series to list
classesList = classesPd.tolist()
xCenterList = []
yCenterList = []
boxLengthList = []
boxWidthList = []
goodRows = []
goodClasses = []

uniqueClasses = set(classesList)
uniqueClassesList = list(uniqueClasses)
uniqueClassesList.sort()
uniqueIDs = set(imgIDs)

for i in range(0, len(imgIDs)):  #  geospatial to YOLO (norm by img size, [0,1])
    # for i in range(0, 1):
    fName = imgIDs[i]
    # Get Excel ID into format of file ID
    fName = fName + "-VIS.ntf.r0"
    fName = fName.lstrip("NITFVIS")
    fName = fName[:14] + "-" + fName[14:]

    if fName in listFiles:  # Only deal with files in tar 00
        # Open file
        fPath = "C:/Purdue/LeGrand/EO/" + fName
        dataset = gdal.Open(fPath)
        band = dataset.GetRasterBand(1)

        xPixels = band.XSize  # is how many pixels in left to right
        yPixels = band.YSize  # is how many pixels up to down
        # Location of bbox center
        xProportion = xCenter[i] / xPixels
        yProportion = yCenter[i] / yPixels

        className = classesPd[i]
        classID = uniqueClassesList.index(className)
        # Need to convert meters of bounding box into geospatial coords, and then can convert to pixels
        # Means need to convert geographic coords (WGS84) to a local CRS
        # Wright-Patterson is in UTM 16S north
        # Procedure: convert center of bbox from WGS84 to UTM, +/- 0.5 * track length to easting and +/- 0.5 track width to northing.
        # Returns four points at center of each edge of bbox. Convert each point to pixel position, and difference gives width/height
        # Anyway to use 16S rather than just 16 north?
        utmProj = Proj("+proj=utm +zone=16 +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
        utmX, utmY = utmProj(trackLong[i], trackLat[i])  # Convert center of bbox to UTM
        # Find center of bbox edges in UTM
        utmXRight = utmX + 0.5 * boxLength[i]
        utmXLeft = utmX - 0.5 * boxLength[i]
        utmYTop = utmY + 0.5 * boxWidth[i]
        utmYBot = utmY - 0.5 * boxWidth[i]
        # Put four edges of bbox back into WGS84
        lonTop, latTop = utmProj(utmX, utmYTop, inverse=True)
        lonRight, latRight = utmProj(utmXRight, utmY, inverse=True)
        lonBot, latBot = utmProj(utmX, utmYBot, inverse=True)
        lonLeft, latLeft = utmProj(utmXLeft, utmY, inverse=True)

        geotransform = dataset.GetGeoTransform()
        # Get geospatial distance between top left corner and bbox
        geoDiffLonTop = lonTop - geotransform[0]
        geoDiffLonRight = lonRight - geotransform[0]
        geoDiffLonBot = lonBot - geotransform[0]
        geoDiffLonLeft = lonLeft - geotransform[0]

        geoDiffLatTop = geotransform[3] - latTop
        geoDiffLatRight = geotransform[3] - latRight
        geoDiffLatBot = geotransform[3] - latBot
        geoDiffLatLeft = geotransform[3] - latLeft
        # Convert geospatial distance to pixel distance by dividing by geotransform[1/5]
        # Convert pixel distance to proportion of image with dividing by dataset.RasterX/YSize
        imgXTop = geoDiffLonTop / (geotransform[1] * dataset.RasterXSize)
        imgXRight = geoDiffLonRight / (geotransform[1] * dataset.RasterXSize)
        imgXBot = geoDiffLonBot / (geotransform[1] * dataset.RasterXSize)
        imgXLeft = geoDiffLonLeft / (geotransform[1] * dataset.RasterXSize)

        imgYTop = geoDiffLatTop / (-geotransform[5] * dataset.RasterYSize)
        imgYRight = geoDiffLatRight / (-geotransform[5] * dataset.RasterYSize)
        imgYBot = geoDiffLatBot / (-geotransform[5] * dataset.RasterYSize)
        imgYLeft = geoDiffLatLeft / (-geotransform[5] * dataset.RasterYSize)
        # Get width/height of bounding box with difference
        bboxWidth = imgXRight - imgXLeft
        bboxHeight = abs(imgYTop - imgYBot)

        # If label file already exists, append; else, create it
        fileName = "C:/Purdue/LeGrand/EOlabelsCorrected/" + imgIDs[i] + ".txt"
        if os.path.isfile(fileName):
            with open(fileName, "a") as f:  # Append as new row to existing file
                label = (
                    "\n"
                    + str(classID)  # Class number
                    + " "
                    + str(xProportion)  # x location
                    + " "
                    + str(yProportion)  # y location
                    + " "
                    + str(bboxWidth)  # bounding box width
                    + " "
                    + str(bboxHeight)  # bounding box height
                )
                f.write(label)
        else:
            with open(fileName, "w") as f:  # Write new file
                label = (
                    str(classID)
                    + " "
                    + str(xProportion)  # x location
                    + " "
                    + str(yProportion)  # y location
                    + " "
                    + str(bboxWidth)  # bounding box width
                    + " "
                    + str(bboxHeight)  # bounding box height
                )
                f.write(label)
