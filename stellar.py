# -*- coding: utf-8 -*-
"""
stellarPY
@file: primary
@author: Brunston Poon
@org: UH-IFA / SPS
@namingConvention: lowerCamelCase
"""

import numpy as np
import math
from scipy import ndimage
from PIL import Image
from matplotlib import pyplot as plt
import pdb
import sys

"""
figure 0: pixelDistribution
figure 1: intensity
figure 2: regression from spectrum against points
"""

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

def intensityR(img, data, regArray, threshold=110):
    """
    intensityR is the third iteration of the intensity function which aims
    to deal with the plotting of regressed non-orthogonal spectra given in
    an open image img, the pixel data in data, and a regArray generated
    using regression(). Returns a dictionary where key is x value and y
    value is intensity.
    """
    #logging start
    f = open('log_intensity.txt', 'w')
    sys.stdout = f
    np.set_printoptions(threshold=np.nan)
    #//logging start

    lowerx, lowery, upperx, uppery = img.getbbox()
    m, c = regArray[3], regArray[4]
    n = -1 / m
    #background subtraction
    backx = {}
    for x in range(lowerx, upperx):
        for y in range(lowery, uppery):
            pixel = img.getpixel((x,y))
            if pixel[0]+pixel[1]+pixel[2] < threshold:
                backx.append(x)
                backy.append(y) 

    intensities = {} #this is a dictionary.
    for xpixel in range(lowerx, upperx):
        ypixel = m * xpixel + c
        for newx in np.arange(lowerx, upperx - 1, 0.1): #I missed the -1 in iQ
            #newx = modpixel from iQ, newy = crossDispersion from iQ
            newy = n * (newx - xpixel) + ypixel #point-slope, add ypixel ea.side
            if (newy > lowery) and (newy < uppery):
                #anti-aliasing implementation from wiki-spatial-antialiasing.pdf
                #section 2 or in http://is.gd/dnj08y
                for newxRounded in (math.floor(newx), math.ceil(newx)):
                    for newyRounded in (math.floor(newy), math.ceil(newy)):
                        #we need to be sure that the rounded point is in our img
                        if (newyRounded > lowery) and (newyRounded < uppery):
                            percentNewX = 1 - abs(newx - newxRounded)
                            percentNewY = 1 - abs(newy - newyRounded)
                            percent = percentNewX * percentNewY
                            #get antialiased intensity from pixel
                            pixel = img.getpixel((newxRounded,newyRounded))
                            newValue = percent * (pixel[0]+pixel[1]+pixel[2])

                            #to ensure we don't reset a value instead of adding:
                            if xpixel in intensities:
                                intensities[xpixel] = \
                                                    intensities[xpixel] + \
                                                    newValue
                            else:
                                intensities[xpixel] = newValue
                            intensities[xpixel] -= percent * ()
    for xpixel in intensities:
        intensities[xpixel] -= percent
    #logging end
    sys.stdout = sys.__stdout__
    np.set_printoptions(threshold=1000)
    #//logging end

    return intensities
    #rewritten for cleaner reading from intensityQ, regression_test.py provided
    #by Scott and Wikipedia article on spatial antialiasing found at
    #http://is.gd/dnj08y or wiki-spatial-antialiasing.pdf

def plotIntensityR(intensityR):
    plotx, ploty = [], []
    for x in intensityR.keys():
        plotx.append(x)
        ploty.append(intensityR[x])
    plotxn, plotyn = np.array(plotx), np.array(ploty)

    plt.figure(1)
    plt.clf()
    plt.plot(plotx, ploty, 'b--', label='anti-aliased data')
    plt.legend(bbox_to_anchor=(1.05,1), loc = 2, borderaxespad=0.)
    plt.show()

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

def rotate(data, angle):
    """
    Rotates an ndarray data which has already gone through the sumGenerator
    process at an angle (float) given.
    """
    #TODO needs work
    return ndimage.interpolation.rotate(data, angle)

def absResponse(wavelength):
    """
    Would normally have a response function that changes based on the
    wavelength. In this case, a response function has not been found or
    created for the Canon 5D Mk I, so we are using a "response function"
    of 1 across all wavelengths, resulting in no change.
    """
    return 1*wavelength

def regression(img, threshold=127):
    """
    Performs least-squares regression fitting on a given intensityMatrix
    generated using sumGenerator()

    ndarrays are top-left 0,0. To account for this in least-squares regression
    fit, we will use a positional y-value of
    (len of column i.e. numRows) - (y-value )
    """
    #point-gathering code
    lowerx, lowery, upperx, uppery = img.getbbox()
    xvals, yvals = [], []
    for x in range(lowerx, upperx):
        for y in range(lowery, uppery):
            pixel = img.getpixel((x,y))
            if pixel[0]+pixel[1]+pixel[2] > threshold:
                xvals.append(x)
                yvals.append(y) #accounting for upperleft vs lowerleft 0,0
    print(xvals)
    print(yvals)
    #regression code
    xvals_n, yvals_n = np.array(xvals), np.array(yvals)
    A = np.vstack([xvals_n, np.ones(len(xvals_n))]).T
    print("A:\n", A)
    m,c = np.linalg.lstsq(A, yvals_n)[0]
    print("M, C:", m,c)
    return [xvals_n,yvals_n,A,m,c]

def plotRegression(regArray):
    """
    Plots the regression provided against the points provided in the regArray
    """
    x, y, A = regArray[0], regArray[1], regArray[2]
    m, c = regArray[3], regArray[4]


    plt.figure(2)
    plt.clf()
    plt.plot(x, y,'o',label='original data',markersize=4)
    plt.plot(x, m*x + c,'r',linestyle='-', label='fitted line')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()

def crop(image,deletionThreshold=127):
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
