# -*- coding: utf-8 -*-
"""
stellarPY
@file: tests
@author: Brunston Poon
@org: UH-IFA / SPS
"""

import stellar as st
import debug as de
import numpy as np
import scratch as sc
from PIL import Image

path = '127.tiff'
img = Image.open(path)
regArray = st.regression(img)
dataArray = st.converter(path)
st.plotRegression(regArray)
sumArray = st.intensityR(img,dataArray,regArray)
st.plotIntensityR(sumArray)


toggle = False
while toggle == True:
    print("commands (shortnames are first two letters):")
    print("'q', 'quit', 'exit', to exit")
    print("'actual' for actual file, 'sample' for sample")
    print("'regression' for regression test, 'rotate' for rotate test")
    print("'simple' for the simple test")
    blah = input("enter command> ")
    if blah in ("simple","si"): #SIMPLE TEST
        array = de.simpleArray()
        #cropped = st.crop(array, 7)
        #intensity = st.intensity(cropped)
        #st.plotGraph(intensity)
        summed = st.sumGenerator(array)
        regArray = st.regression(summed, 7)
        st.plotRegression(regArray)

    elif blah in ("actual", "ac"): #ACTUAL
        file = 'IMG_2860.tif'
        fileArray = st.converter(file)
        cropped = st.crop(fileArray, 110)
        print("cropped.shape:", cropped.shape)
        #st.restorer(cropped)
        #distribution = st.pixelDistribution(cropped)
        #intensity = st.intensity(cropped)
        #st.plotGraph(intensity)
        # writeLogToFile(fileArray,'log.log')

    elif blah in ("sample", "sa"): #SAMPLE
        test = de.testArray() #will print out the array generated.
        # sums = st.sumGenerator(test)
        # print(sums)
        cropped = st.crop(test)
        print("duplicate returned from crop():\n", cropped)

    elif blah in ("reg", "regression", "re"): #REGRESSION TEST
        testRotate = de.testRotate()
        print("testRotate:\n", testRotate)
        print("testRotate.shape:\n", testRotate.shape)
        regArray = st.regression(testRotate, 0) #test matrix threshold is 0
        st.plotRegression(regArray)

    elif blah in ("rotate", "ro"): #ROTATE TEST
        testRotate = de.testRotate()
        print("testRotate:\n",testRotate)
        rotated = st.rotate(testRotate,30.0)
        print("rotated:\n",rotated)

    elif blah in ("q", "quit", "exit"): break
    else: print("please input a recognized command")
