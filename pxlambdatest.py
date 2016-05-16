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
dataImage = input("file for second image to be adjusted (the data image) ")

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
        
        #TODO debugging text file printing intensity and wavelengths from response
        f = open("debug_wavelengths_intensities_pre-reponse_from-pxlt.txt","w")
        f.write("#values from pxlambdatest.py before feeding to response\n#wavelengths intensity\n")
        for i in range(len(wavelengths)):
            f.write(str(wavelengths[i])+" "+str(intensity[i])+"\n")
        f.close()
        asdfjkl = "asdfjkl"
        print("string before response: ",asdfjkl)
        response = st.response(intensity, wavelengths, "pulkovo/sirius.dat", 0.5,asdfjkl)
        print("len, response: {0}".format(len(response)))
        print(response)
        
        #adjust and display new plot
        adjusted = []
        for i in wavelengths:
            adjusted.append(intensity[i]*response[i])
        adjustedND = np.array(adjusted)
        
        to.plotIntensityWLambda(adjustedND,wavelengths)
        #TODO just realized above convention is confusing. Order of variables
        #     passing to function is (y,x)

        #TODO debugging text files output of plot...
        f = open("debug_first_plot_x_y.txt","w")
        f.write("#X Y\n#wavelengths, adjustedND\n")
        for i in range(len(adjustedND)):
            f.write(str(wavelengths[i])+" "+str(adjustedND[i])+"\n")
        f.close()
        print("debug file of plot that just popped up (adjusted intensity plot)")

        # plt.figure(3)
        # plt.clf()
        # plt.plot(x_star, y_star,'o',label='original data',markersize=4)
        # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        # plt.title("Pulkovo Data from {0}".format(pulkovo))
        # plt.show()

        #TODO DEBUGGING TEXT FILES DEBUGGING TEXT FILES AND IPYTHON
        #TODO remove debugging, examine pulkovoResponse in iPython
        #pulkovoData = np.loadtxt('pulkovo/sirius.dat')
        #for i in range(len(pulkovoData)):
        #    pulkovoData[i][0] = float(pulkovoData[i][0])
        #    pulkovoData[i][1] = float(pulkovoData[i][1])
        #pulkovoResponse = st.response(pulkovoData[:,1], pulkovoData[:,0], "pulkovo/sirius.dat", 1,asdfjkl)
        #first column in pulkovo is equiv to intensity, zeroth wavelength

        #TODO debugging column text files...
        #f = open('debug_response_wavelength.txt','w')
        #f.write("#num wavelengths adjustedND")
        #for i in range(max(len(wavelengths),len(adjustedND))):
        #    f.write(str(i)+" "+str(wavelengths[i])+" "+str(adjustedND[i])+"\n")
        #f.close()
        #print("debug of wavelength and adjustedND to debug_response_wavelength.txt")



    #SECOND IMAGE SECOND IMAGE SECOND IMAGE SECOND IMAGE!!!
    #adjust our second image: convert to data as well as overlay our new
    #adjusted array (to account for camera sensitivity)

    dataImageObject = Image.open(path)
    dataImageArray = to.converter(path)
    
    if showthresh == "yes":
        to.showThreshold(dataArray, threshI)

    print("working on dataImage crop")
    dataImageCropped = st.cropN(dataImageObject, threshI, top, bottom, left,\
                                right, margin)
    to.restorer(dataImageCropped, 'dataImageCropped')
    print("cropped image saved to dataImageCropped.tiff")

    dataImageCroppedObject = Image.open('dataImageCropped.tiff')
    print("converting cropped dataImage")
    dataImageCroppedArray = to.converter('dataImageCropped.tiff')

    regTupDI = st.regression(dataImageCroppedObject)
    to.showRegression(dataImageCroppedObject, regTupDI)

    if autoIntensity in ['saaw']:
        print("working on intensity_saaw. please wait...")

        intensityDI = st.intensitySAAW(dataImageCroppedObject,\
                                       dataImageCroppedArray, regTupDI,\
                                       threshI, step, 10)
        #need to identify wavelengths for target image, see line 69 of file.
        #use with data collected same night to ensure that the other params
        #remain the same (background, clouds, amt of atmosphere in between, etc
