from osgeo import gdal
import sys
import pandas as pd
import matplotlib.pyplot as plt
import cv2 as cv
import os, os.path

if __name__ == "__main__":
    listFiles = os.listdir("C:\Purdue\LeGrand\EO")
    numFiles = len(listFiles)
    #print(numFiles) #3000 files
    i = 0
    while i < 3000: 
        fName = listFiles[i]
        fPath = "C:/Purdue/LeGrand/EO/" + fName
        
        dataset = gdal.Open(fPath)
        band = dataset.GetRasterBand(1)
        scanlineArray = band.ReadAsArray(0, 0, dataset.RasterXSize, 
		dataset.RasterYSize, dataset.RasterXSize, dataset.RasterYSize)

        fNameClean = (fName.replace("-", ""))
        fNameClean = fNameClean.rstrip("0") #Otherwise strip ending numbers as well
        fNameClean = fNameClean.rstrip("VIS.ntf.r")
        fNameClean = "NITFVIS" + fNameClean

        #plt.imshow(scanlineArray, cmap=plt.cm.gray) #shows image
        #plt.show()

        cv.imwrite("C:/Purdue/LeGrand/EOjpg/" + fNameClean + ".jpg", scanlineArray)
    
        i += 6 #Only use .r0 versions
        #print(i)