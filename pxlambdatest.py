# -*- coding: utf-8 -*-
"""
stellarPYL - python stellar spectra processing software
Copyright (c) 2016 Brunston Poon
@file: pxlambda test
This program comes with absolutely no warranty.
"""

import configparser

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

import stellar as st
import tools as to
import text as txt
config = configparser.ConfigParser()
config.read('settings.ini')
defThresh = config['CONTROL']['defaultthreshold']
autoIntensity = config['CONTROL']['autointensity']
top = int(config['CONTROL']['manualtop'])
bottom = int(config['CONTROL']['manualbot'])
right = int(config['CONTROL']['manualright'])
left = int(config['CONTROL']['manualleft'])
step = float(config['CONTROL']['r'])
verbose = config['CONTROL']['verbose']
showthresh = config['CONTROL']['showthresh']
margin = int(config['CONTROL']['margin'])

print("""
We need a file. Place it in the same directory as this script and give the name.
    """)
path = input("enter filename> ")

threshI = int(defThresh)
if threshI >= 0:
    print("converting. please wait...")

    img = Image.open(path)
    dataArray = to.converter(path)

    if showthresh == "yes":
        to.showThreshold(dataArray, threshI)

    print("working on crop. please wait...")
    cropped = st.cropN(img, threshI, top, bottom, left, right, margin)
    to.restorer(cropped, 'cropped')
    print("cropped image saved to cropped.tiff")

    croppedimg = Image.open('cropped.tiff')
    print("converting cropped image. please wait...")
    dataArray = to.converter('cropped.tiff')

    regTup = st.regression(croppedimg)
    to.showRegression(croppedimg,regTup)

    if autoIntensity in ['saaw']:
        print("working on intensity_saaw. please wait...")

        intensity = st.intensitySAAW(croppedimg,dataArray,regTup,\
                                     threshI,step,10)
        #TODO remove debugging
        for element in intensity:
            print(element)
        #using IMG_2617.tif of sirius and using hA = beta, hB = gamma b/c of
        #apparent visibles.
        wavelengths = to.pixelLambda(intensity, 515, 627)
        #print(wavelengths)
        to.plotIntensityWLambda(intensity,wavelengths)
        #to.plotIntensityWLambda2(intensity,wavelengths)
        #to.plotSamples(croppedimg,intensity,regTup) #TODO fix
        response = st.response(intensity, wavelengths, "pulkovo/sirius.dat", 0.5)
        print("len, response: {0}".format(len(response)))
        print(response)
        
        #adjust and display new plot
        adjusted = []
        for i in wavelengths:
            adjusted.append(intensity[i]*response[i])
        adjustedND = np.array(adjusted)
        
        to.plotIntensityWLambda(adjustedND,wavelengths)
        # plt.figure(3)
        # plt.clf()
        # plt.plot(x_star, y_star,'o',label='original data',markersize=4)
        # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        # plt.title("Pulkovo Data from {0}".format(pulkovo))
        # plt.show()
