# -*- coding: utf-8 -*-
"""
stellarPY
@file: tools
@author: Brunston Poon
@org: UH-IFA / SPS
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
    config['CONTROL'] = {'defaultthreshold':'-1',
                         'autointensity':'saa',
                         'manualtop':'-1',
                         'manualbot':'-1',
                         'manualleft':'-1',
                         'manualright':'-1',
                         'r':'1',
                         'verbose':'no',
                         'showthresh':'yes',
                         'margin':'5'}
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
    centerX, centerY = 544, 12
    box = (centerX-10,centerY-10,centerX+10,centerY+10)
    boximg = img.crop(box)
    boximg.load()
    bigbox = boximg.resize((210,210))
    m, c, x, y = st.regression(bigbox)
    n = -1/m
    step = math.sqrt((r**2) / (1 + m**2))

    lowerx, lowery, upperx, uppery = bigbox.getbbox()
    for xpixel in np.linspace(lowerx, upperx,num=math.ceil((upperx/step)+1)):
        ypixel = m * xpixel + c
        for newx in np.arange(lowerx, upperx - 1, 1):
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
                            if v=='yes': print("using pixel {0},{1}".format(\
                                                newxRounded,newyRounded))
                            #dotted line?
                            if (newxRounded % 2) == 0:
                                imgpixels[newxRounded, newyRounded] = (88,252,238)
        pbar(xpixel/upperx) #progress bar
    plt.imshow(bigbox)
    plt.show()
    return None
    
def plotIntensity(intensity):
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
    plt.plot(plotx, ploty, 'b-', label='anti-aliased data')
    plt.legend(bbox_to_anchor=(1.05,1), loc = 2, borderaxespad=0.)
    plt.savefig('intensity.png', bbox_inches='tight')
    plt.show()
    
    print("\nfigure saved to intensity.png")

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