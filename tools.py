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
    return Non

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