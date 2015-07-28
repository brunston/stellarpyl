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
    print("""
Type 'q', 'quit', or 'exit' to leave this program. Alternately, you may use
ctrl-c to force-interrupt at any time. This text is also available online at
http://st.brunston.net/ or by viewing README.md

IF YOU ARE A NEW USER, PLEASE READ THIS ENTIRE BODY OF TEXT.

This is stellar spectra reduction and analysis command-line software written
using the Python 3.4 version of the Anaconda Scientific Python distribution. It 
is work done for an internship at the Unversity of Hawaii in conjunction with 
the St. Paul's School Engineering Honors program.

It aims to provide a one-click workflow for analyzing uncompressed TIFF stellar
spectra images obtained from a DSLR through a diffraction grating. The goals of
the project are: to automatically crop the image; to perform background 
subtraction; to create an intensity plot of the spectrum (accounting for non-
orthogonal spectra); and to account for the use of a DSLR sensor by using either
a relative response function or an absolute response function to normalize the 
intensity plot.

TO VIEW HELP, TYPE 'help', which will run through a typical workflow scenario.
TYPE 'functions' to view all the functions available to you with explanations.

            """)

while toggle == True:
    validCommands = ("pixel_d", "image_regression", \
                    "intensity_n", "intensity_saa", \
                    "pd", "imgreg", "saa", "n", "crop")
    userInput = input("enter command> ")
    if userInput in ("help"):
        print("""
You will be presented with a list of commands.

For a brand new image, run 'crop' first. Drag your file into the same directory
and enter the filename including the file extension. This program will accept
TIFF files, either in .tif or .tiff extension format. It will then ask you for a
threshold.

The threshold is used throughout the program to determine what data is relevant
and what parts of the image can be discarded without damaging the value of the
data. It needs to be an integer value between 0 and 765 as the threshold is
measured as the sum of the R, G, and B bin values in a pixel, therefore, 
each RGB value can be an integer from 0-255; total value can be from 0-765. If
you do not have a value you are already using for all of your images, you can
type 'pixel_d' at the command prompt to run a function that plots the
distribution of binned pixel values in your image.

The program will run the cropping algorithm and ask for a filename to give to
the new file.

The next command you should run is 'intensity_saa'. It will take an image file
and a threshold and automatically perform linear regression to find the y=mx+b
line on which the spectral trace lies. It will then step one pixel at a time
along the spectral trace and add up all intensity values occuring along that
line.

The program will graph this intensity plot, which can be saved using the tools
already provided by matplotlib.
            """)

    if userInput in ("functions"):
        print("""

- 'pixel_d' (short 'pd') -
takes an image and shows the pixel distribution of the image over the intensity
of the pixels.

- 'crop' - 
takes an image and crop it based on your selected threshold.

- 'image_regression' (short 'imgreg') -
takes an image and finds the line which goes through the spectrum in that image.

- 'intensity_n' (short 'n') -
takes an image of a spectrum and converts it into an intensity plot using the
naive method of adding.

- 'intensity_saa' (short 'saa') -
takes an image of a spectrum and converts it into an intensity plot using
spatial anti-aliasing at a sub-sampling rate of one tenth of one pixel.

            """)

    if userInput in validCommands:
        print("\
                We need a file. Place it in the same directory\n \
                as this script and give the name.")
        path = input("enter filename> ")
        print("converting. please wait...")
        img = Image.open(path)
        dataArray = to.converter(path)
        print("Your answer to the following depends for all commands except\n \
'pixel_d'.")

        print("What threshold would you like to use as differentiator?")
        thresh = input("enter threshold> ")
        threshI = int(thresh)

        if userInput in ("intensity_saa", "saa"):
            print("working on intensity_saa. please wait...")
            regTup = st.regression(img)
            intensity = st.intensitySAAN(img,dataArray,regTup, threshI)
            to.plotIntensity(intensity)

        if userInput in ("intensity_n", "n"):
            print("working on intensity_n. please wait...")
            regTup = st.regression(img)
            intensity = st.intensityN(img,dataArray,regTup, threshI)
            to.plotIntensity(intensity)

        if userInput in ("image_regression", "imgreg"):
            print("working on image_regression. please wait...")
            regTup = st.regression(img)
            to.plotRegression(regTup)

        if userInput in ("pixel_d", "pd"):
            print("working on pixel_distribution. please wait...")
            to.pixelDistribution(dataArray)

        if userInput in ("crop"):
            print("working on crop. please wait...")
            cropped = st.crop(img, threshI)
            filename = input("filename for cropped? DO NOT ADD EXTENSION> ")
            to.restorer(cropped, filename)
            print("file has been created at: ", filename + ".tiff")

        print("""
Type 'q', 'quit', or 'exit' to leave this program. Alternately, you may use
ctrl-c to force-interrupt at any time. Type 'help' for sample workflow and
'functions' for a list of functions.
            """)

    elif userInput in ("q", "quit", "exit"):
        break

    elif userInput in ("jellyfish"):
            print("""
                
                                        (hello!)
                                      .'
                                     '
                      _ -- ~~~ -- _      _______
                  .-~               ~-.{__-----. :
                /                       \      | |
               :         O     O         :     | |
               /\                       /------' j
              { {/~-.      \__/      .-~\~~~~~~~~~
               \/ /  |~:- .___. -.~\  \  \.
              / /\ \ | | { { \ \  } }  \  \.
             { {   \ \ |  \ \  \ \ /    } }
              \ \   /\ \   \ \  /\ \   { {
               } } { { \ \  \ \/ / \ \  \ \.
              / /   } }  \ \ }{ {    \ \ } }
             / /   { {     \ \{\ \    } { {
            / /     } }     } } \  / / \ \ \.
           `-'     { {     `-'\ \`-'/ /   `-'
                    `-'        `-' `-'

                    unknown artist
                """)

    else:
        print("Please input a recognized command.")
