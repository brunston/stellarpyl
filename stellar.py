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
import statistics
from PIL import Image
from matplotlib import pyplot as plt
import tools as to

import pdb
import sys

def backMedian(img, threshold):
    """
    calculates the median value of 'blackness' in an image under a specific
    threshold
    """
    lowerx, lowery, upperx, uppery = img.getbbox()
    back = []
    for x in range(lowerx, upperx):
        for y in range(lowery, uppery):
            pixel = img.getpixel((x,y))
            pixelSum = pixel[0]+pixel[1]+pixel[2]
            if pixelSum < threshold:
                back.append(pixelSum)
    backMedian = statistics.median(back)
    return backMedian

def intensityN(img, data, reg, threshold = 127):
    """
    Creates a 'proper' intensity array for the data given in a numpy array and
    using an open Image given in img. Degree offset is calculated by a
    y = mx + c function as done in regression()
    regArray = [xvals_n, yvals_n, A, m, c]
    """
    lowerx, lowery, upperx, uppery = img.getbbox()
    m, c = reg[0:2]
    n = -1 / m
    #background subtraction median calculation
    back = backMedian(img, threshold)
    print("running intensityN")
    intensities = {} #this is a dictionary.
    for xpixel in range(lowerx, upperx):
        ypixel = m * xpixel + c
        for newx in np.arange(lowerx, upperx - 1, 0.1): #I missed the -1 in iQ
            #newx = modpixel from iQ, newy = crossDispersion from iQ
            newy = n * (newx - xpixel) + ypixel #point-slope, add ypixel ea.side
            if (newy > lowery) and (newy < uppery):
                #anti-aliasing implementation http://is.gd/dnj08y
                for newxRounded in (math.floor(newx), math.ceil(newx)):
                    for newyRounded in (math.floor(newy), math.ceil(newy)):
                        #we need to be sure that the rounded point is in our img
                        if (newyRounded > lowery) and (newyRounded < uppery):
                            pixel = img.getpixel((newxRounded,newyRounded))
                            newValue = pixel[0]+pixel[1]+pixel[2]
                            #to ensure we don't reset a value instead of adding:
                            if xpixel in intensities:
                                intensities[xpixel] = \
                                                    intensities[xpixel] + \
                                                    newValue
                            else:
                                intensities[xpixel] = newValue
                                intensities[xpixel] -= back
        to.pbar(xpixel/upperx) #progress bar

    return intensities
    #rewritten for cleaner reading from intensityQ, regression_test.py provided
    #by Scott and Wikipedia article on spatial antialiasing found at
    #http://is.gd/dnj08y or wiki-spatial-antialiasing.pdf

def intensitySAAN(img, data, reg, threshold=127):
    """
    intensitySAAN is the fourth iteration of the intensity function which aims
    to deal with the plotting of regressed non-orthogonal spectra given in
    an open image img, the pixel data in data, and a regArray generated
    using regression(). Returns a dictionary where key is x value and y
    value is intensity.
    """
    lowerx, lowery, upperx, uppery = img.getbbox()
    m, c = reg[0:2]
    n = -1 / m
    #background subtraction median calculation
    back = backMedian(img, threshold)

    intensities = {} #this is a dictionary.
    angle = np.arctan(m)
    step = math.sqrt((1 / (1 + m**2)))
    print("running intensitySAA")
    for xpixel in np.linspace(lowerx, upperx,num=math.ceil((upperx/step)+1)):
        ypixel = m * xpixel + c
        for newx in np.arange(lowerx, upperx - 1, 0.1): #I missed the -1 in iQ
            #newx = modpixel from iQ, newy = crossDispersion from iQ
            newy = n * (newx - xpixel) + ypixel #point-slope, add ypixel ea.side
            if (newy > lowery) and (newy < uppery):
                #anti-aliasing implementation http://is.gd/dnj08y
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
                            intensities[xpixel] -= percent * back
        to.pbar(xpixel/upperx) #progress bar


    return intensities
    #rewritten for cleaner reading from intensityQ, regression_test.py provided
    #by Scott and Wikipedia article on spatial antialiasing found at
    #http://is.gd/dnj08y or wiki-spatial-antialiasing.pdf

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

def regression(img, threshold=127):
    """
    Performs least-squares regression fitting on a given image.
    Returns a tuple: (m,c,xvals_n,yvals_n). tuple[0:2] for just (m,c)
    """
    #point-gathering code
    lowerx, lowery, upperx, uppery = img.getbbox()
    xvals, yvals = [], []
    print("running regression")
    for x in range(lowerx, upperx):
        for y in range(lowery, uppery):
            pixel = img.getpixel((x,y))
            if pixel[0]+pixel[1]+pixel[2] > threshold:
                xvals.append(x)
                yvals.append(y) #accounting for upperleft vs lowerleft 0,0
        to.pbar(x/(upperx+1)) #not 100%
    #regression code
    xvals_n, yvals_n = np.array(xvals), np.array(yvals)
    A = np.vstack([xvals_n, np.ones(len(xvals_n))]).T
    m,c = np.linalg.lstsq(A, yvals_n)[0]
    #print("M, C:", m,c)
    to.pbar(1) #100%
    return (m,c,xvals_n, yvals_n)

def crop(image,deletionThreshold=127):
    """
    Crops image based on the number of empty pixels [0,0,0]
    Crops top-to-bottom, bottom-to-top, right-to-left, and then left-to-right
    based on the way that the current set of data has been collected.
    """
    duplicate = np.copy(image)
    #print("duplicate:\n", duplicate)
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
            #print("cropping row:", a)

    print("beginning bottom crop, top ran fine")
    to.pbar(.25)

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
            #print("cropping row:", a)

    print("\nbeginning right->left crop, bottom ran fine")
    to.pbar(.5)

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
            #print("cropping col:", a)

    print("\nbeginning left->right crop, right->left ran fine")
    to.pbar(.75)
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
            #print("cropping col:", a)

    #troubleshooting
    #print("duplicate shape:", duplicate.shape)
    #print("duplicate dtype:", duplicate.dtype)
    print("\n")
    to.pbar(1)
    return duplicate
