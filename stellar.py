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
    counterPerRow = 0
    for i in range(len(duplicate[0])): #goes by pixel in row
        if np.array_equal(duplicate[0][i], np.array([0,0,0])):
            #adds to counter if pixel is empty
            counterPerRow = counterPerRow + 1
        # else:
        #     print("breaking")
        #     print("duplicate:\n", duplicate)
        #     break
        if counterPerRow == len(duplicate[0]):
            #if whole row is empty, delete the row in question
            duplicate = np.delete(duplicate, 0, 0)
            print("Cropping row 0")
            crop(duplicate)
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
