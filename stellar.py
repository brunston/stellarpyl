# -*- coding: utf-8 -*-
"""
stellarPY
@file: primary
@author: Brunston Poon
@org: UH-IFA / SPS
"""

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import pdb

def converter(imageToConvert):
    """
    Converts image given in filepath format as tif to a numpy array and returns
    """
    #note- for some reason, Lightroom-cropped tif files do not play nice.
    #Use original files.

    image = Image.open(imageToConvert)
    imageArray = np.array(image)

    #troubleshooting statements
    print("ndarray imageArray:\n", imageArray)
    print("imageArray shape:", imageArray.shape)
    print("imageArray dtype:", imageArray.dtype)

    return imageArray

def crop(image):
    """
    Crops image based on the number of empty pixels [0,0,0]
    Crops top-to-bottom, right-to-left, bottom-to-top, and then left-to-right
    based on the way that the current set of data has been collected.
    """
    duplicate = np.copy(image)
    print("duplicate:\n", duplicate)
    counterPerRow = 0
    numRow = len(duplicate)
    numCol = len(duplicate[0])

    #row[i] = duplicate[i]
    #column[j] = duplicate[:,j]

    #cropping from top
    while True:
        numRow = len(duplicate)
        a = 0
        for i in range(numCol):
            if not np.array_equal(duplicate[a][i], np.array([0,0,0])):

                pdb.set_trace()
                break
            else:
                counterPerRow += 1
        if counterPerRow == len(duplicate[a]):
            #if the entire row of pixels is empty, delete row
            duplicate = np.delete(duplicate, 0, 0)
            print("cropping row:", a)
            print("New duplicate:\n", duplicate)
        else:#fix
            break#thesetwolines 

    #cropping from bottom
    # while True:
    #     numRow = len(duplicate)
    #     a = numRow-1
    #     for i in range(numCol):
    #         if not np.array_equal(duplicate[a][i], np.array([0,0,0])):
    #             #adds to counter if iterated pixel is empty
    #
    #             pdb.set_trace()
    #             break
    #         else:
    #             counterPerRow += 1
    #     if counterPerRow == len(duplicate[a]):
    #         #if the entire row of pixels is empty, delete row
    #         duplicate = np.delete(duplicate, 0, 0)
    #         print("cropping row:", a)
    #         print("New duplicate:\n", duplicate)
    #     else:
    #         break

    print("duplicate right before return:\n", duplicate)
    return duplicate

def intensity(data,degreeOffset):
    """
    Creates an intensity array for the data given in a numpy array. Also allows
    for the insertion of an absolute response function.
    degreeOffset (float) refers to the offset of the data from the horizontal.
    Counter-clockwise (i.e. 'above horizontal') is positive
    Clockwise (i.e. 'below horizontal') is negative
    """
    intensity = []
    if degreeOffset == 0: #i.e. we just want to add vertically
        for k in range(len(data[0])): #goes by column
            vertSlice = data[:,k] # a single column k with all rows
            #print("vertSlice:\n", vertSlice)
            runningTotal = 0
            for pixel in vertSlice:
                for color in pixel:
                    runningTotal = color + runningTotal
            intensity.append(runningTotal)
    intensityNP = np.array(intensity)
    return intensityNP

def plotGraph(intensity):
    """
    Plots the intensity array generated
    """
    x = []
    for i in range(len(intensity)):
        #instead of pixel values as is by simply appending 0,1,2, this portion
        #of the function can be set up to use a wavelength-to-pixel ratio.
        x.append(i*1)
    xNP = np.array(x)
    plt.figure(0)
    plt.clf() #clears figure
    plt.plot(xNP, intensity,'b.',markersize=4)
    plt.title("intensity plot, intensity vs wavelength")
    plt.xlbl("wavelength (nm)")
    plt.ylbl("intensity (8-bit pixel addition)")


def absResponse(wavelength):
    """
    Would normally have a response function that changes based on the
    wavelength. In this case, a response function has not been found or
    created for the Canon 5D Mk I, so we are using a "response function"
    of 1 across all wavelengths, resulting in no change.
    """
    return 1*wavelength
