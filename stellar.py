# -*- coding: utf-8 -*-
"""
stellarPY
@file: primary
@author: Brunston Poon
@org: UH-IFA / SPS
@namingConvention: lowerCamelCase
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
    # print("ndarray imageArray:\n", imageArray)
    print("imageArray shape:", imageArray.shape)
    print("imageArray dtype:", imageArray.dtype)

    return imageArray

def restorer(arrayToConvert):
    """
    Converts array given as ndarray to a tif and returns None
    """
    image = Image.fromarray(arrayToConvert)
    image.save("image.tiff", "TIFF")
    return None

def pixelDistribution(data):
    """
    Creates a plot which shows the relative pixel distribution of data given
    in ndarray format so that we can figure out how much "noise" is feasible
    to get rid of without harming the rest of the data
    """
    numRow = len(data)
    numCol = len(data[0])
    distributionArray = np.zeros(766, dtype=np.uint8)
    x = np.arange(765+1)
    for row in range(numRow):
        for col in range(numCol):
            pixelSum = np.sum(data[row][col])
            distributionArray[pixelSum] += 1

    plt.figure(0)
    plt.clf() #clears figure
    plt.plot(x, distributionArray,'b.',markersize=4)
    return distributionArray


def intensity(data,degreeOffset=0):
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
    Plots the intensity array generated and returns None
    """
    x = []
    for i in range(len(intensity)):
        #instead of pixel values as is by simply appending 0,1,2, this portion
        #of the function can be set up to use a wavelength-to-pixel ratio.
        x.append(i*1)
    xNP = np.array(x)
    plt.figure(1)
    plt.clf() #clears figure
    plt.plot(xNP, intensity,'b.',markersize=4)
    plt.title("intensity plot, intensity vs wavelength")
    plt.xlbl("wavelength (nm)")
    plt.ylbl("intensity (8-bit pixel addition)")
    return None

def sumGenerator(data):
    """
    Creates a 2d matrix of intensity values from a given ndarray data which
    has values in uint8 RGB form
    """
    new = []
    for row in data:
        rowArray = []
        for pixel in row:
            pixelSum = 0
            for value in pixel:
                pixelSum += value
            rowArray.append(pixelSum)
        new.append(rowArray)
    newNP = np.array(new)
    return newNP

def absResponse(wavelength):
    """
    Would normally have a response function that changes based on the
    wavelength. In this case, a response function has not been found or
    created for the Canon 5D Mk I, so we are using a "response function"
    of 1 across all wavelengths, resulting in no change.
    """
    return 1*wavelength

# def identifyTargetPixels(data):
#     """
#     Identifies target pixels much like the relevant/non-relevant indicator
#     in the crop() function. Takes data as ndarray, uint8
#     """
#     for row in data:
#         for pixel in row:

# def regression(intensityMatrix):
#     """
#     Performs least-squares regression fitting on a given intensityMatrix
#     generated using sumGenerator()
#     """
#     x,y = [], []
#     x = np.arange(len(intensityMatrix[0])


def crop(image):
    """
    Crops image based on the number of empty pixels [0,0,0]
    Crops top-to-bottom, bottom-to-top, right-to-left, and then left-to-right
    based on the way that the current set of data has been collected.
    """
    duplicate = np.copy(image)
    print("duplicate:\n", duplicate)
    #these get initialized now and updated in each while loop.
    numCol = len(duplicate[0]) #number of columns in image
    numRow = len(duplicate) #number of rows in image
    deletionThreshold = 127 #threshold for the
    #cropping from top
    toggleTop = True
    while toggleTop == True:
        numRow = len(duplicate)
        a = 0
        counterPerRow = 0
        for i in range(numCol):
            if not (np.sum(duplicate[a][i]) <= deletionThreshold):
                toggleTop = False
                break
            # if not np.array_equal(duplicate[a][i], np.array([0,0,0])):
            #     toggleTop = False
            #     break
            else:
                counterPerRow += 1
        if counterPerRow == len(duplicate[a]):
            #if the entire row of pixels is empty, delete row
            duplicate = np.delete(duplicate, a, 0)
            print("cropping row:", a)
        # else: #is this else redundant?
        #     #will the first 'if not' catch all that we need to catch?
        #     toggle = False

    print("beginning bottom crop, top ran fine")

    #cropping from bottom
    toggleBot = True
    while toggleBot == True:
        numRow = len(duplicate)
        a = numRow-1
        counterPerRow = 0
        for i in range(numCol):
            if not (np.sum(duplicate[a][i]) <= deletionThreshold):
                toggleBot = False
                break
            # if not np.array_equal(duplicate[a][i], np.array([0,0,0])):
            #     toggleBot = False
            #     break
            else:
                counterPerRow += 1
        if counterPerRow == numCol:
            #if the entire row of pixels is empty, delete row
            duplicate = np.delete(duplicate, a, 0)
            print("cropping row:", a)
        # else: #is this else redundant?
        #     #will the first 'if not' catch all that we need to catch?
        #     toggle = False

    print("beginning right->left crop, bottom ran fine")

    #cropping from right to left
    toggleRight = True
    while toggleRight == True:
        numRow = len(duplicate)
        numCol = len(duplicate[0]) #needs to be updated each time loop iterates
        a = numCol - 1
        counterPerCol = 0
        for i in range(numRow):
            if not (np.sum(duplicate[i][a]) <= deletionThreshold):
                toggleRight = False
                break
            # if not np.array_equal(duplicate[i][a], np.array([0,0,0])):
            #     #note the reverse of the i and a ^^ for vertical crop
            #     toggleRight = False
            #     break
            else:
                counterPerCol += 1
        if counterPerCol == numRow:
            #if the entire col of pixels is empty, delete col
            duplicate = np.delete(duplicate, a, 1)
            print("cropping col:", a)

    print("beginning left->right crop, right->left ran fine")
    #cropping from left to right
    toggleLeft = True
    while toggleLeft == True:
        numRow = len(duplicate)
        numCol = len(duplicate[0]) #needs to be updated each time loop iterates
        a = 0
        counterPerCol = 0
        for i in range(numRow):
            if not (np.sum(duplicate[i][a]) <= deletionThreshold):
                toggleLeft = False
                break
            # if not np.array_equal(duplicate[i][a], np.array([0,0,0])):
            #     #note the reverse of the i and a ^^ for vertical crop
            #     toggleLeft = False
            #     break
            else:
                counterPerCol += 1
        if counterPerCol == numRow:
            #if the entire col of pixels is empty, delete col
            duplicate = np.delete(duplicate, a, 1)
            print("cropping col:", a)

    #troubleshooting
    print("duplicate shape:", duplicate.shape)
    print("duplicate dtype:", duplicate.dtype)

    return duplicate
