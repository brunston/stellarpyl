# -*- coding: utf-8 -*-
"""
stellarPY
@file: ui
@author: Brunston Poon
@org: UH-IFA / SPS
"""

#Let's make sure that the user has all the dependencies installed and that
#they are running the correct version of Python
toggle = True
try:
    import numpy as np
    from PIL import Image
except ImportError:
    "numpy and PIL are not installed. Please install before continuing."
    toggle = False

import sys
version = sys.version_info[0]
if version != 3:
    "Please upgrade to Python3, preferably 3.4.* or greater"
    toggle = False

#import the rest
import stellar as st
import tools as to


if toggle == True:
    print("\
            Type 'q', 'quit', or 'exit' to leave this program. Alternately,\n \
            you may use ctrl-c to force-interrupt at any time. Your options\n \
            are available--:'pixel_d', 'image_regression', 'intensity_n'\n \
            'intensity_saa', or 'crop'. See http://st.brunston.net or README\n \
            for appropriate documentation.")

while toggle == True:
    validCommands = ("pixel_d", "image_regression", \
                    "intensity_n", "intensity_saa", \
                    "pd", "imgreg", "saa", "n", "crop")
    userInput = input("enter command> ")
    if userInput in validCommands:
        print("\
                We need a file. Place it in the same directory\n \
                as this script and give the name.")
        path = input("enter filename> ")
        img = Image.open(path)
        regTup = st.regression(img)
        dataArray = to.converter(path)
        print("Your answer to the following depends for all commands except\n \
                'pixel_d'.")
        print("What threshold would you like to use as differentiator?")
        thresh = input("enter threshold> ")
        if userInput in ("intensity_saa", "saa"):
            intensity = st.intensitySAA(img,dataArray,regTup, int(thresh))
            to.plotIntensity(intensity)
        if userInput in ("intensity_n", "n"):
            intensity = st.intensityN(img,dataArray,regTup, int(thresh))
            to.plotIntensity(intensity)
        if userInput in ("image_regression", "imgreg"):
            to.plotRegression(regTup)
        if userInput in ("pixel_d", "pd"):
            to.pixelDistribution(dataArray)
        if userInput in ("crop"):
            st.crop(img, thresh)
        print("\
            Type 'q', 'quit', or 'exit' to leave this program. Alternately,\n \
            you may use ctrl-c to force-interrupt at any time. Your options\n \
            are available--:'pixel_d', 'image_regression', 'intensity_n'\n \
            'intensity_saa', or 'crop'. See http://st.brunston.net or README\n \
            for appropriate documentation.")
    elif userInput in ("q", "quit", "exit"):
        break
    else:
        print("Please input a recognized command.")
