# -*- coding: utf-8 -*-
"""
stellarPYL - python stellar spectra processing software
Copyright (c) 2016 Brunston Poon
@file: tools
This program comes with absolutely no warranty.
"""
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

#required for plotIntensityWLambda2
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
#from astropy.io import fits
#fits files are messed up if gotten from VizieR and pulkovo

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

def plotIntensityW(intensity, linetype='b-'):
    """
    Plots an intensity graph with connected points for SAAW
    """
    plotx, ploty = [], []
    i = 0
    for x in range(len(intensity)):
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

def plotIntensityWLambda(intensity,wavelengths, linetype='b-'):
    """
    Plots intensity graph with connected points for SAAW and pixelLambda
    """
    plotx, ploty = [], []
    i = 0
    for x in range(len(intensity)):
        plotx.append(wavelengths[x])
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

def plotIntensityWLambda2(intensity,wavelengths, linetype='b-'):
    """
    Plots intensity graph with connected points for SAAW and pixelLambda
    This is the version with two axes (one with pixels, one with nm)
    """
    plotx, ploty = [], []
    i = 0
    for x in range(len(intensity)):
        plotx.append(wavelengths[x])
        ploty.append(intensity[x])

    plotxn, plotyn = np.array(plotx), np.array(ploty)
    host = host_subplot(111,axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75)
    
    par1 = host.twinx()
    par2 = host.twinx()
    
    offset = 60
    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    
    par2.axis['bot'] = new_fixed_axis(loc='right',axes=par2,offset=(offset,0)
    par2.axis['bott'].toggle(all=True)
    
    par1.set_xlabel
    plt.plot(plotx, ploty, linetype)
    plt.legend(bbox_to_anchor=(1.05,1), loc = 2, borderaxespad=0.)
    plt.savefig('intensity.png', bbox_inches='tight')
    plt.show()

    print("\nfigure saved to intensity.png")
    return None

def plotSamples(img, intensity, reg, offsetTuple, xMap, yMap, point=200.):
    """
    Plots samples for some point along the intensity given
    """
    lowerx, lowery, upperx, uppery = img.getbbox()
    m, c = reg[0:2]
    q = m * point + c
    print("offsetTuple,", offsetTuple)
    offsetVertical = offsetTuple[0]
    offsetTrace = offsetTuple[1]
    print("img",img)
    imageArray = np.asarray(img)
    print("img as ndarray", img)
    imFlipped = np.flipud(imageArray)
    xmin,xmax,ymin,ymax = 30,700,0,40
    imCropped = imFlipped[ymin:ymax,xmin:xmax,:]
    imgplot = plt.imshow(imCropped)
    plotSetting = 111

    #TODO add plotSetting as well as other features from sampling sample
    #  select a subset of the image to use, and scale it
    # xmin = 0
    # xmax = 800
    # ymin = 0
    # ymax = 55

    perp_m = -1.0 / m
    perp_c = q + point/m

    xTrace = np.arange(1.0*xmin,xmax)
    yTrace = m * xTrace + c
    print(img)
    #imgplot = plt.imshow((img), zorder = 0, extent = [xmin,xmax,ymin,ymax])
    ax2 = plt.subplot(plotSetting)
    ax2.plot(xTrace,yTrace, color='red')
    plt.show()

    # perpendicular
    ax3 = plt.subplot(plotSetting)
    ax3.plot(point, q, color='white', marker='*', markersize=20)
    plt.show()

    xPerp = 1.0*np.arange(point - 20, point + 20)
    yPerp = perp_m * xPerp + perp_c
    ax4 = plt.subplot(plotSetting)
    ax4.plot(xPerp, yPerp, color='red', linestyle='dashed')
    plt.show()

    yPerpHigh = yPerp + offsetTrace
    ax5 = plt.subplot(plotSetting)
    ax5.plot(xPerp, yPerpHigh, color='white', linestyle='dashed')
    plt.show()

    yPerpLow = yPerp - offsetTrace
    ax6 = plt.subplot(plotSetting)
    ax6.plot(xPerp, yPerpLow, color='white', linestyle='dashed')
    plt.show()

    yTraceHigh = yTrace + offsetVertical
    ax7 = plt.subplot(plotSetting)
    ax7.plot(xTrace, yTraceHigh, color='white', linestyle='dashed')
    plt.show()

    yTraceLow = yTrace - offsetVertical
    ax8 = plt.subplot(plotSetting)
    ax8.plot(xTrace, yTraceLow, color='white', linestyle='dashed')
    plt.show()

    #  show all nearby possible points
    subpoints = np.where((np.abs(xMap - point) < 20) & (np.abs(yMap - q) < 20))
    ax9 = plt.subplot(plotSetting)
    ax9.scatter(xMap[subpoints], yMap[subpoints], color='black', marker='.')
    plt.show()

    #  show all points within the box
    include = np.where((yMap < ((-1.0/m)*xMap + perp_c + offsetTrace)) & \
                       (yMap >= ((-1.0/m)*xMap + perp_c - offsetTrace)) & \
                       (yMap < (m*xMap + c + offsetVertical)) & \
                       (yMap >= (m*xMap + c - offsetVertical)))
    ax10 = plt.subplot(plotSetting)
    ax10.scatter(xMap[include],yMap[include], color='red', marker='o')
    plt.show()
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

def comparer(star):
    """
    Grab the regression from the pulkovo catalog data in pulkovo/
    http://vizier.cfa.harvard.edu/viz-bin/Cat?III/201
    Actually, can use single star data by searching for a particular star to
    load data from.
    """
    #TODO Currently should only be importing from Sirius. Make generalized later

    starData = np.loadtxt("pulkovo/sirius.dat")
    #above imports as ndarray of 2-item ndarrays

    #fitsList = fits.open("pulkovo/stars.fits")
    #stars = np.loadtxt("pulkovo/stars.dat")
    return None

def pixelLambda(intensities, pixelA, pixelB):
    """
    Converts intensities to wavelength values based on particular intensities
    being identified as Hydrogen Balmer lines alpha and beta, where halpha
    and hbeta are the positional values within intensities
    """
    nmA = 656.3
    nmB = 486.1
    nmG = 434.1
    pixelAB = abs(pixelB - pixelA) # difference between halpha and hbeta in pixels
    nmPixel = (nmB - nmG) / pixelAB #ratio nm to pixels #TODO BG IS TEMP
    wavelengths = [] #empty array

    c = nmB - (nmPixel)*pixelB
    print(c)
    for pixel in range(len(intensities)):
        value = nmPixel*pixel + c
        print(value)
        wavelengths.append(value)
        #above from rise/run equations
    wavelengthsND = np.array(wavelengths)
    return wavelengthsND
