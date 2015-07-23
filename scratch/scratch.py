# -*- coding: utf-8 -*-
"""
stellarPY
@file: scratch testing
@author: Brunston Poon
@org: UH-IFA / SPS
"""

import numpy as np
from PIL import Image
import sys
import math
from matplotlib import pyplot as plt

import stellar as st
import debug as de

def calcOne(img,data,regArray):
    f = open('log_intensity.txt', 'w')
    sys.stdout = f
    np.set_printoptions(threshold=np.nan)
    m, c = regArray[3], regArray[4]
    #LETS CALCULATE THE VALUE OF THE LINE AT X=5 ON THE LONG AXIS
    lowerx, lowery, upperx, uppery = img.getbbox()
    xpixel = 100
    ypixel = m * xpixel + c

    lineArray = []
    n = -1/m
    for modpixel in np.arange(lowerx, upperx, 0.1):
        print("+ a pixel from modpixel, value: ", modpixel)
        crossDispersion = n * (modpixel - xpixel) + ypixel
        print("pixel (%.2f,%.2f)" %(modpixel, crossDispersion))
        if (crossDispersion > lowery) and (crossDispersion < uppery):
            lineArray.append([round(modpixel), round(crossDispersion)])
            print("appended pixel successfully")
    lineArrayn = np.array(lineArray)
    print("sumArrayn:\n", lineArrayn)

    #logging end
    sys.stdout = sys.__stdout__
    np.set_printoptions(threshold=1000)

    return lineArrayn

def dispOne(lineArray):
    x = []
    y = []
    for element in lineArray:
        x.append(element[0])
        y.append(element[1])
    plt.figure(3)
    plt.clf() #clears figure
    plt.plot(x, y,'b.',markersize=4)
    plt.title("dispOne")


#Playing with numpy ndarray slicing
# test = de.testArray()
# print("testArray, without modification or selection:\n", test)
# print("test[0]:\n",test[0])
# print("test[:0]:\n",test[:0])
# print("test[:,:15]:\n", test[:,:15])
# #test[:,:15] produces all of the pixels in each row up to the 15th column
# print("test[:,15]:\n", test[:,15])
# #SUCCESS! This will produce the 15th column across all the rows. This is great
# #because not only will it work for cropping but it  will also help in adding
# #all of the pixel values in the column.
#
# #TIF importation using pillow/PIL
# """
# The importation of the tif using PIL works like this: Each row in the
# array array[i] is a list of lists. Each list in the list (array[i][j]) is
# a list of 3 values where each value refers to the RGB value (HAVE TO FIND
# OUT IF IT IS IN THAT ORDER).
# """

# def identifyTargetPixels(data):
#     """
#     Identifies target pixels much like the relevant/non-relevant indicator
#     in the crop() function. Takes data as ndarray, uint8
#     """
#     for row in data:
#         for pixel in row: