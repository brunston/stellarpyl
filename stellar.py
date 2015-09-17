# -*- coding: utf-8 -*-
"""
stellarPYL - python stellar spectra processing software
Copyright (c) 2015 Brunston Poon
@file: stellar
This program comes with absolutely no warranty.
"""

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

import tools as to

import pdb
import sys
import configparser

import math
import statistics

config = configparser.ConfigParser()
config.read('settings.ini')
v = config['CONTROL']['verbose'] #enables or disables printing of debug

def backMedian(img, threshold):
    """
    calculates the median value of 'blackness' in an image under a specific
    threshold
    """

    lowerx, lowery, upperx, uppery = img.getbbox()
    back = []
    print("calculating backMedian")

    for x in range(lowerx, upperx):
        for y in range(lowery, uppery):
            pixel = img.getpixel((x,y))
            pixelSum = pixel[0]+pixel[1]+pixel[2]

            if pixelSum < threshold:
                back.append(pixelSum)

        to.pbar(x/upperx)

    to.pbar(1)
    backMedian = statistics.median(back)

    return backMedian

def intensityN(img, data, reg, threshold = 127,r=1):
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
    if v=='yes': print("backMedian:", back)
    print("running intensityN")
    intensities = {} #this is a dictionary.
    step = math.sqrt((r**2) / (1 + m**2))

    for xpixel in np.arange(lowerx, upperx, step):
        ypixel = m * xpixel + c
        for newx in np.arange(lowerx, upperx - 1, 0.1):
            newy = n * (newx - xpixel) + ypixel #point-slope, add ypixel ea.side

            if (newy > lowery) and (newy < uppery):
                #anti-aliasing implementation http://is.gd/dnj08y

                for newxRounded in (math.floor(newx), math.ceil(newx)):
                    for newyRounded in (math.floor(newy), math.ceil(newy)):
                        #we need to be sure that the rounded point is in our img
                        if (newyRounded > lowery) and (newyRounded < uppery):
                            pixel = img.getpixel((newxRounded,newyRounded))

                            if v=='yes': print("using pixel {0},{1}".format(\
                                                newxRounded,newyRounded))

                            newValue = pixel[0]+pixel[1]+pixel[2]
                            #to ensure we don't reset a value instead of adding:
                            to.addElement(intensities, xpixel, newValue)
                            intensities[xpixel] -= back
        to.pbar(xpixel/upperx) #progress bar
    
    if v=='yes': print("intensities:", intensities)

    return intensities

def intensitySAAN(img, data, reg, threshold=127, r=1):
    """
    intensitySAAN is the fourth iteration of the intensity function which aims
    to deal with the plotting of regressed non-orthogonal spectra given in
    an open image img, the pixel data in data, and a regArray generated
    using regression().
    SAA - spatial antialiasing; N - new
    Returns a dictionary where key is x value and y
    value is intensity.
    r is the step rate along the spectral trace (default to size of one pixel)
    """
    
    lowerx, lowery, upperx, uppery = img.getbbox()
    m, c = reg[0:2]
    n = -1 / m
    #background subtraction median calculation
    back = backMedian(img, threshold)
    if v=='yes': print("backMedian:", back)
    print("running intensitySAAN")
    intensities = {} #this is a dictionary.
    angle = np.arctan(m)
    step = math.sqrt((r**2) / (1 + m**2))
    #for xpixel in np.linspace(lowerx, upperx,num=math.ceil((upperx/step)+1)):

    for xpixel in np.arange(lowerx, upperx, step):
        ypixel = m * xpixel + c
        for newx in np.arange(lowerx, upperx - 1, 0.1):
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

                            if v=='yes': print("using pixel {0},{1}".format(\
                                                newxRounded,newyRounded))
                            if v=='yes': print("value being added:",newValue)

                            #to ensure we don't reset a value instead of adding:
                            to.addElement(intensities, xpixel, newValue)

                            intensities[xpixel] -= percent * back
        to.pbar(xpixel/upperx) #progress bar

    if v=='yes': print("intensities:", intensities)

    return intensities

def intensitySAANB(img, data, reg, threshold=127, r=1, twidth=10,spss=0.1):
    """
    intensitySAANB is the sixth iteration of the intensity function which aims
    to deal with the plotting of regressed non-orthogonal spectra given in
    an open image img, the pixel data in data, and a regArray generated
    using regression().
    SAA - spatial antialiasing; NB - new, box method
    Returns a dictionary where key is x value and y value is intensity.
    r is the step rate along the spectral trace (default to size of one pixel)
    twidth is the width of the trace on each side of the line y = mx + c
    so the total will be double
    spss is the subpixel sampling size
    """
    
    lowerx, lowery, upperx, uppery = img.getbbox()
    m, c = reg[0:2]
    n = -1 / m
    back = backMedian(img, threshold)

    if v=='yes': print("backMedian:", back)
    print("running intensitySAANB")

    intensities = {} #this is a dictionary.
    angle = np.arctan(m)
    step = r * np.cos(angle)

    for x in np.arange(lowerx, upperx, step):
        y = m * x + c
        upperLimitX, lowerLimitX = x + (step/2), x - (step/2)

        for y2 in np.arange(lowery,uppery,1):
            #a refers to a point (a,b) on the perp line to mx+c passing thru
            #both x and y2
            a = ((y2 - y) / n) + x
            ulima, llima = math.floor(a + (step/2)), math.ceil(a - (step/2))
            ulimaNR, llimaNR = a + (step/2), a - (step/2) #NR = No Rounding

            for x2 in np.arange(lowerx,upperx,1):

                if (x2 < ulima) and (x2 > llima):
                    pixel = img.getpixel((x2,y2))
                    to.addElement(intensities, x2, pixel)

                if (x2 == ulima) or (x2 == llima):
                    pixel = img.getpixel((x2,y2))
                    subpixelCounter = 0
                    totalPossibleSubpixels = (1/spss)**2

                    if x2 == ulima:
                        for subpixely in np.arange(x2, x2+1,spss):
                            for subpixelx in np.arange(x2,x2+1,spss):
                                if subpixelx <= ulimaNR:
                                    subpixelCounter += 1

                    if x2 == llima:
                        for subpixely in np.arange(x2, x2+1,spss):
                            for subpixelx in np.arange(x2,x2+1,spss):
                                if subpixelx >= llimaNR:
                                    subpixelCounter += 1

                    percentage = subpixelCounter / totalPossibleSubpixels
                    newValue = pixel * percentage
                    to.addElement(intensities, x2, newValue)

        to.pbar(xpixel/upperx) #progress bar

    if v=='yes': print("intensities:", intensities)

    return intensities

def parallel(m, b, d):
    return b - (d / math.sqrt(1 / m * m + 1)) * (m - 1 / m)
def inverseF(m, y, b):
    return (y - b) / m

def intensitySAANS(img, data, reg, threshold=127, r=1, twidth=10,spss=0.1):
    """
    temp imp SAANB
    """
    x1, y1, x2, y2 = img.getbbox()
    m, c = reg[0:2]
    n = -1 / m
    back = backMedian(img, threshold)
    WIDTH = 3
    perpendiculars = []    
    for p in np.arange(x1, x2, 0.1):
    # Calculate the corresponding y coordinate to p (called q) on our long axis, from our regression, where y = mx + b.
    # (p, q) is a point on our long axis.
        q = m * p + c
        # Slope of perpendicular is -1 / m, it's Y intercept is the value of the function at p.
        perp_m = -1 / m
        perp_c = q
        perpendiculars.append((p, perp_c, parallel(perp_m, perp_c, -WIDTH), parallel(perp_m, perp_c, WIDTH)))
    SAMPLING_FACTOR = 0.50
    for x in np.arange(x1, x2, SAMPLING_FACTOR):
        for y in np.arange(y1, y2, SAMPLING_FACTOR):
            # For all the perpendiculars to our long axis.
            for perp in perpendiculars:   
                # Determine if x is between the lines around the perpendicular.
                if x > inverseF(n, y, perp[2]) and x < inverseF(n, y, perp[3]):
                    pixel = image.getpixel((math.floor(x), math.floor(y)))
                    intensity = (pixel[0] + pixel[1] + pixel[2]) * SAMPLING_FACTOR
                    p = perp[0]

                    # If we have a value for this x value (known as p) on our long axis, then add it to what we've got.
                    # Remember that the same p value will be picked for multiple intensities since we are using fractional nx's.
                    if p in intensities:
                        intensities[p] = intensities[p] + intensity
                    else:
                        intensities[p] = intensity
    for graphx in intensities.keys():
    a.append(graphx)
    b.append(intensities[graphx])


    x, y = np.array(a), np.array(b)
    plt.plot(x, y, 'o', label='Original data', markersize=10)
    plt.show()
    return None


def sumGenerator(data):
    """
    Creates a 2d matrix of intensity values from a given ndarray data which
    has values in uint8 RGB form
    """
    new = []
    print("creating 2d array from 3d tiff RGB array")
    pbarCounter = 0
    for row in data:
        rowArray = []
        for pixel in row:
            pixelSum = 0
            for value in pixel:
                pixelSum += value
            rowArray.append(pixelSum)
        new.append(rowArray)
        to.pbar(pbarCounter/len(data))
        pbarCounter += 1
    to.pbar(1)
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
            if (pixel[0]+pixel[1]+pixel[2]) > threshold:
                xvals.append(x)
                yvals.append(y)
        to.pbar(x/(upperx+1)) #not 100%
    #regression code

    xvals_n, yvals_n = np.array(xvals), np.array(yvals)
    A = np.vstack([xvals_n, np.ones(len(xvals_n))]).T
    m,c = np.linalg.lstsq(A, yvals_n)[0]

    to.pbar(1) #100%
    if v=='yes': print("M, C:", m,c)
    return (m,c,xvals_n, yvals_n)

def cropN(image, threshold,\
          manualTop, manualBot, manualLeft, manualRight, margin):
    """
    Crops image data based on pixels falling below or above a certain threshold.
    This is an updated version of crop which uses the np.where() command.
    Crops while considering manual overrides for the cropping limits.
    """
    print("cropping image")
    data = np.array(image)
    simplifiedData = sumGenerator(data)
    yAboveThreshold, xAboveThreshold = np.where(simplifiedData > threshold)
    #setting the bounds of the image to be min and max of where the image has
    #pertinent data. Also, adds a margin.
    lowerx, upperx = np.amin(xAboveThreshold), np.amax(xAboveThreshold)
    lowery, uppery = np.amin(yAboveThreshold,), np.amax(yAboveThreshold)

    manualTop, manualBot = manualTop, manualBot
    manualLeft, manualRight = manualLeft, manualRight

    if v=='yes':
        print("lx,ux,ly,uy:{0},{1},{2},{3}".format(lowerx,upperx,lowery,uppery))
    
    #making sure we will not go out of bounds
    for thing in (lowerx, lowery):
        if not ((thing - margin) < 0):
            if v=='yes': print("{0} margin clear! incl margin".format(thing))
            thing -= margin
        else:
            if v=='yes': print("{0} margin not clear! using orig".format(thing))

    for thing in (upperx, uppery):
        if not ((thing + margin) > (len(simplifiedData) - 1)):
            if v=='yes': print("{0} margin clear! incl margin".format(thing))
            thing += margin
        else:
            if v=='yes': print("{0} margin not clear! using orig".format(thing))

    #let's check to see if we need to override using the manual selection
    if (lowerx > manualLeft) and (manualLeft != -1):
        if v=='yes': print("overriding left")
        lowerx = manualLeft

    if (upperx < manualRight) and (manualRight != -1):
        if v=='yes': print("overriding right")
        upperx = manualRight

    if (lowery > manualTop) and (manualTop != -1):
        if v=='yes': print("overriding top")
        lowery = manualTop

    if (uppery < manualBot) and (manualBot != -1):
        if v=='yes': print("overriding bot")
        uppery = manualBot

    finalSelection = data[lowery:(uppery+1),lowerx:(upperx+1)]
    if v=='yes': print("Final selection from {0} to {1} in x, \
                        from {2} to {3} in y.".format(\
                        lowerx, upperx, lowery, uppery))

    return finalSelection


def crop(image,deletionThreshold,autostopTB, autostopBT, autostopRL, autostopLR):
    """
    (deprecated)
    Crops image based on the number of empty pixels [0,0,0]
    Crops top-to-bottom, bottom-to-top, right-to-left, and then left-to-right
    based on the way that the current set of data has been collected.
    autostops will stop at a specific column if requested.
    """
    duplicate = np.copy(image)
    #print("duplicate:\n", duplicate)
    #these get initialized now and updated in each while loop.
    numCol = len(duplicate[0]) #number of columns in image
    numRow = len(duplicate) #number of rows in image
    #cropping from top
    toggleTop = True
    autostopCounterT = 0
    while toggleTop == True:
        a = 0
        counterPerRow = 0
        for i in range(numCol):
            if not (np.sum(duplicate[a][i]) <= deletionThreshold):
                toggleTop = False
                break
            else:
                counterPerRow += 1
        if counterPerRow == len(duplicate[a]):
            #if the entire row of pixels is empty, delete row
            duplicate = np.delete(duplicate, a, 0)
            #print("cropping row:", a)
        if autostopCounterT == autostopTB:
            toggleTop = False
            break
        autostopCounterT += 1

    print("beginning bottom crop, top ran fine")
    to.pbar(.25)

    #cropping from bottom
    toggleBot = True
    autostopCounterB = 0
    while toggleBot == True:
        numRow = len(duplicate)
        a = numRow-1
        counterPerRow = 0
        for i in range(numCol):
            if not (np.sum(duplicate[a][i]) <= deletionThreshold):
                toggleBot = False
                break
            else:
                counterPerRow += 1
        if counterPerRow == numCol:
            #if the entire row of pixels is empty, delete row
            duplicate = np.delete(duplicate, a, 0)
            #print("cropping row:", a)
        if autostopCounterB == autostopBT:
            toggleBot = False
            break
        autostopCounterB += 1

    print("\nbeginning right->left crop, bottom ran fine")
    to.pbar(.5)

    #cropping from right to left
    toggleRight = True
    autostopCounterR = 0
    while toggleRight == True:
        numRow = len(duplicate)
        numCol = len(duplicate[0]) #needs to be updated each time loop iterates
        a = numCol - 1
        counterPerCol = 0
        for i in range(numRow):
            if not (np.sum(duplicate[i][a]) <= deletionThreshold):
                toggleRight = False
                break
            else:
                counterPerCol += 1
        if counterPerCol == numRow:
            #if the entire col of pixels is empty, delete col
            duplicate = np.delete(duplicate, a, 1)
            #print("cropping col:", a)
        if autostopCounterR == autostopRL:
            toggleRight = False
            break
        autostopCounterR += 1

    print("\nbeginning left->right crop, right->left ran fine")
    to.pbar(.75)
    #cropping from left to right
    toggleLeft = True
    autostopCounterL = 0
    while toggleLeft == True:
        numRow = len(duplicate)
        numCol = len(duplicate[0]) #needs to be updated each time loop iterates
        a = 0
        counterPerCol = 0
        for i in range(numRow):
            if not (np.sum(duplicate[i][a]) <= deletionThreshold):
                toggleLeft = False
                break
            else:
                counterPerCol += 1
        if autostopCounterL == autostopLR:
            toggleLeft = False
            break
        if counterPerCol == numRow:
            #if the entire col of pixels is empty, delete col
            duplicate = np.delete(duplicate, a, 1)
            #print("cropping col:", a)
        autostopCounterL += 1
    #troubleshooting
    #print("duplicate shape:", duplicate.shape)
    #print("duplicate dtype:", duplicate.dtype)
    print("\n")
    to.pbar(1)
    return duplicate
