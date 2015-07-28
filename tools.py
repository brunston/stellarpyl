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
import time
import sys

"""
figure 0: pixelDistribution
figure 1: intensity
figure 2: regression from spectrum against points
"""


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
    text = "\rProgress: [{0}] {1}% {2}".format( "#"*block + "-"*(barlen-block),\
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
    # print("ndarray imageArray:\n", imageArray)
    #print("imageArray shape:", imageArray.shape)
    #print("imageArray dtype:", imageArray.dtype)

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

def plotIntensity(intensity):
    plotx, ploty = [], []
    for x in intensity.keys():
        plotx.append(x)
        ploty.append(intensity[x])
    plotxn, plotyn = np.array(plotx), np.array(ploty)

    plt.figure(1)
    plt.clf()
    plt.plot(plotx, ploty, 'b-', label='anti-aliased data')
    plt.legend(bbox_to_anchor=(1.05,1), loc = 2, borderaxespad=0.)
    plt.show()
    plt.savefig('intensity.png', bbox_inches='tight')

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