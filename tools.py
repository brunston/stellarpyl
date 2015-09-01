# -*- coding: utf-8 -*-
"""
stellarPYL - python stellar spectra processing software
Copyright (c) 2015 Brunston Poon
@file: tools
This program comes with absolutely no warranty.
"""
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

import sys
import configparser

import time
import math

import stellar as st


"""
figure 0: pixelDistribution
figure 1: intensity
figure 2: regression from spectrum against points
"""
config = configparser.ConfigParser()
config.read('settings.ini')
v = config['CONTROL']['verbose'] #enables or disables printing of debug

def configDefault():
    config = configparser.ConfigParser()
    config['CONTROL'] = {'defaultthreshold':'127',
                         'autointensity':'saa',
                         'manualtop':'-1',
                         'manualbot':'-1',
                         'manualleft':'-1',
                         'manualright':'-1',
                         'r':'1',
                         'verbose':'no',
                         'showthresh':'yes',
                         'margin':'5',
                         'firstrun':'yes'}
    with open('settings.ini','w') as cfile:
        config.write(cfile)

def pbar(progress):
    """
    Python progress bar
    Accepts a float between 0 and 1. Any int will be converted to a float.
    A value under 0 represents a 'halt'. A value at 1 or bigger represents 100%
    modified from http://is.gd/bKdMvT answer by Brian Khuu
    """
    barlen = 20 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if progress >= 1:
        progress = 1
        status = "Done.\r\n"
    elif progress < 0:
        progress = 0
        status = "Halt.\r\n"
    block = int(round(barlen*progress))
    text = "\rProgress: [{0}] {1}% {2}".format( "A"*block + "h"*(barlen-block),\
                                                progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

def converter(imageToConvert):
    """
    Converts image given in filepath format as tif to a numpy array and returns
    """
    #note- for some reason, Lightroom-cropped tif files do not play nice.
    #Use original files.

    image = Image.open(imageToConvert)
    imageArray = np.array(image)

    #troubleshooting statements
    if v=='yes':
        print("ndarray imageArray:\n", imageArray)
        print("imageArray shape:", imageArray.shape)
        print("imageArray dtype:", imageArray.dtype)

    return imageArray

def restorer(arrayToConvert, fname):
    """
    Converts array given as ndarray to a tif and returns None
    """

    image = Image.fromarray(arrayToConvert)
    fnameWithExtension = fname + ".tiff"
    image.save(fnameWithExtension, "TIFF")

    return None

def addElement(dictn, element, value):
    """
    adds value to element in dictionary dictn. if already present, adds value
    to existing value of element
    """
    if element in dictn:
        dictn[element] = dictn[element] + value
    else:
        dictn[element] = value

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
    print("generating pixelDistribution")

    for row in range(numRow):
        for col in range(numCol):
            pixelSum = np.sum(data[row][col])
            distributionArray[pixelSum] += 1
        pbar(row/numRow)

    plt.figure(0)
    plt.clf() #clears figure
    plt.plot(x, distributionArray,'b.',title="pixel distribution", markersize=4)
    plt.show()

    return distributionArray

def showThreshold(data, threshold):
    """
    shows what exactly counts in the threshold when applying to data
    """

    numRow = len(data)
    numCol = len(data[0])
    print("running showThreshold")
    numPixels = 0

    for row in range(numRow):
        for col in range(numCol):
            pixelSum = np.sum(data[row][col])
            if pixelSum <= threshold:
                data[row][col] = [255, 153, 102]
                numPixels += 1
        pbar(row/numRow)
    img = Image.fromarray(data)
    img.save("showThreshold.tiff", "TIFF")
    pbar(1)

    print("You can see what has been selected by viewing showThreshold.tiff")
    if v=='yes': print("Number of pixels under threshold: ",numPixels)

    return None

def showRegression(img, reg):
    """
    shows regressed line overlayed on the original (cropped) image.
    """
    print("running showRegression")

    lowerx, lowery, upperx, uppery = img.getbbox()
    m, c, x, y = reg

    plt.figure(2)
    plt.imshow(img)
    plt.plot(x, m*x + c,'r',linestyle='-', \
             label='fitted line, y = {0}x + {1}'.format(m,c))
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.axis('off')
    plt.savefig('regression.png', bbox_inches='tight')
    plt.show()
    print("figure saved to regression.png")

    return None

def showWalks(img, reg, centerpoint=70, r=1):
    """
    shows walking lines overlayed on the original (cropped) image.
    """
    print("running showWalks")

    lowerx, lowery, upperx, uppery = img.getbbox()
    centerX, centerY = 554, 50
    box = (centerX-10,centerY-10,centerX+10,centerY+10) #creates a 21x21 image
    boximg = img.crop(box)
    boximg.load()
    bigbox = boximg.resize((210,210))
    imgpixels = bigbox.load()

    m, c, x, y = st.regression(bigbox)
    plt.plot(x, m*x + c,'r',linestyle='-', label='fitted line')

    print("m: {0} c: {1} ".format(m,c))

    n = -1/m
    step = math.sqrt((r**2) / (1 + m**2))
    lowerx, lowery, upperx, uppery = bigbox.getbbox()
    colors = [(155, 89, 182), (241, 196, 15), (231, 76, 60),\
              (26, 188, 156), (46, 204, 113), (230, 126, 34), (52, 152, 219)]

    for xpixel in np.linspace(lowerx, upperx,num=math.ceil((upperx/step)+1)):
        ypixel = m * xpixel + c
        for newx in np.arange(lowerx, upperx - 1, 4):
            newy = n * (newx - xpixel) + ypixel #point-slope, add ypixel ea.side
            if (newy > lowery) and (newy < uppery):
                imgpixels[math.floor(newx), \
                          math.floor(newy)] = colors[math.floor(newx)%6]
        pbar(xpixel/upperx) #progress bar
    plt.imshow(bigbox)
    plt.savefig('walks.png', bbox_inches='tight')
    plt.show()

    return None
    
def plotIntensity(intensity, linetype='b-'):
    """
    Plots an intensity graph with connected points
    """
    plotx, ploty = [], []
    for x in intensity.keys():
        plotx.append(x)
        ploty.append(intensity[x])
    plotxn, plotyn = np.array(plotx), np.array(ploty)

    plt.figure(1)
    plt.clf()
    plt.plot(plotx, ploty, linetype)
    plt.legend(bbox_to_anchor=(1.05,1), loc = 2, borderaxespad=0.)
    plt.savefig('intensity.png', bbox_inches='tight')
    plt.show()
    
    print("\nfigure saved to intensity.png")
    return None

def plotRegression(reg):
    """
    Plots the regression provided against the points provided in the regArray
    """
    m,c,x,y = reg

    plt.figure(2)
    plt.clf()
    plt.plot(x, y,'o',label='original data',markersize=4)
    plt.plot(x, m*x + c,'r',linestyle='-', label='fitted line')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()

    return None