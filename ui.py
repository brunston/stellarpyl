# -*- coding: utf-8 -*-
"""
stellarPY
@file: ui
@author: Brunston Poon
@org: UH-IFA / SPS
"""

#Let's make sure that the user has all the dependencies installed and that
#they are running the correct version of Python
import os
import sys
import configparser
import time

toggle = True
version = sys.version_info[0]

if version != 3:
    print("Please upgrade to Python3, preferably 3.4.* or greater")
    toggle = False
    os._exit(1)

try:
    import numpy as np
    from PIL import Image
except ImportError:
    print("numpy and PIL are not installed. Please install before continuing.")
    toggle = False
    os._exit(1)

#import the rest
import stellar as st
import tools as to

if toggle == True:
    config = configparser.ConfigParser()
    config.read('settings.ini')
    print("""
Type 'q', 'quit', or 'exit' to leave this program. Alternately, you may use
ctrl-c to force-interrupt at any time. This text is also available online at
http://st.brunston.net/ or by viewing README.md

TO VIEW HELP, WHICH WILL RUN THROUGH A TYPICAL WORKFLOW SCENARIO, TYPE 'help'.

TO VIEW A LIST OF AVAILABLE FUNCTIONS & COMMANDS, TYPE 'commands'.

TO LEARN MORE ABOUT THIS PROGRAM, TYPE 'about'.

            """)

while toggle == True:
    #update settings
    config.read('settings.ini')
    defThresh = config['CONTROL']['defaultThreshold']
    autoIntensity = config['CONTROL']['autoIntensity']
    TB = config['CONTROL']['autoStopTB']
    BT = config['CONTROL']['autoStopBT']
    RL = config['CONTROL']['autoStopRL']
    LR = config['CONTROL']['autoStopLR']
    step = float(config['CONTROL']['r'])

    prgmCommands = ("pixel_d", "image_regression", \
                    "intensity_n", "intensity_saa", \
                    "pd", "imgreg", "saa", "n", "crop", "show_threshold",\
                    "show_regression", "show_walks")

    userInput = input("enter command> ")

    #TEXT COMMANDS NEXT
    if userInput in ["about"]:
        print("""
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
            """)
    if userInput in ["help"]:
        print("""

AS AN ALTERNATIVE TO THE BELOW, make sure you set a default threshold using
'settings_threshold', and then simply type 'auto' to have the program do
the majority of the work.

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

    if userInput in ["commands"]:
        print("""
            ---IMAGE PROCESSING---
- 'autoProcess' (short 'auto') -
autoProcess will take care of cropping and doing intensity plotting for you.
just provide a filename. In order to use this feature you must first set
a default threshold to use by using the 'settings_threshold' command.

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

- 'show_threshold' -
see exactly what could be removed (assuming no crop stop has been set) using the
threshold that is currently set.

- 'show_regression' -
shows regressed line overlayed on the original (cropped) image.

- 'show_walks' -
shows walking lines overlayed on the original (cropped) image.

            ---PROGRAM---

- 'about' -
displays information about this program

- 'functions' -
where you are now

- 'help' -
brings up sample workflow

- 'settings_default' -
returns ALL settings back to default:
    defaultThreshold = -1
    autoIntensity = saa

- 'settings_intensity' -
sets default intensity processing method for the autoProcess feature.
The default setting is saa (for spatial anti-aliasing).

- 'settings_step'
sets default step value along the spectral trace (and thus resolution of
resulting intensity plot). default is 1 pixel-equivalence.

- 'settings_stop' -
stops crop at a specific column set here. use the TB (top to bottom) BT, RL, or
LR settings to cut off the auto-crop at a certain column in a certain direction.
The default is -1 for all values (no autostop).

- 'settings_threshold' -
sets default threshold. Set to -1 if you would like the program to always ask.
The default setting is -1 (always asks).

- 'view_settings' -
view your current settings

            """)
    

    #AUTOPROCESS
    if userInput in ['autoProcess', 'auto']:
        print("""
We need a file. Place it in the same directory as this script and give the name.
            """)
        path = input("enter filename> ")
        timeStart = time.time()
        threshI = int(defThresh)
        if threshI >= 0:
            print("converting. please wait...")
            img = Image.open(path)
            dataArray = to.converter(path)
            timePause0 = time.time()
            to.show_threshold(data, threshI)
            timePause0s = time.time()
            print("working on crop. please wait...")
            cropped = st.crop(img, threshI, TB, BT, RL, LR)
            to.restorer(cropped, 'cropped')
            croppedimg = Image.open('cropped.tiff')
            print("converting cropped image. please wait...")
            dataArray = to.converter('cropped.tiff')
            regTup = st.regression(croppedimg)
            timePause1 = time.time()
            to.showRegression(croppedimg,regTup)
            timePause1s = time.time()
            if autoIntensity in ['saa']:
                print("working on intensity_saa. please wait...")
                intensity = st.intensitySAAN(croppedimg,dataArray,regTup,threshI,step)
                timePause2 = time.time()
                to.plotIntensity(intensity)
                timePause2s = time.time()
            if autoIntensity in ['n']:
                print("working on intensity_n. please wait...")
                intensity = st.intensityN(croppedimg,dataArray,regTup,threshI,step)
                timePause2 = time.time()
                to.plotIntensity(intensity)
                timePause2s = time.time()
            timeEnd = time.time()
            print("Total time required:", timeEnd-(timePause0s-timePause0)\
                                          -(timePause1s-timePause1)\
                                          -(timePause2s-timePause2)-timeStart)
        else:
            print("defaultThreshold not set. aborting.")


    #HOUSEKEEPING COMMANDS NEXT
    if userInput in ["settings_default"]:
        while True:
            print("ARE YOU SURE YOU WANT TO RESET SETTINGS? CANNOT BE UNDONE!")
            query = input("type 'yes'/'no'> ")
            if query in ['yes']:
                to.configDefault()
                print("Set settings to default.")
                break
            elif query in ['no']:
                print("Keeping settings as is.")
                break
            else:
                print("please type 'yes' or 'no'")

    if userInput in ["settings_intensity"]:
        print("""
sets default intensity processing method for the autoProcess feature.
AVAILABLE OPTIONS: 'saa' (spatial anti-aliasing), 'n' (naive). Default is 'saa'.
            """)
        query = input("Set default autoProcess intensity> ")
        if query in ['saa', 'n']:
            config['CONTROL']['autoIntensity'] = query
            with open('settings.ini', 'w') as cfile:
                config.write(cfile)
            print("Set new setting of: ",query)
        else:
            print("not an acceptable value. no value set.")

    if userInput in ["settings_threshold"]:
        print("""
sets a default threshold for any function of this program requiring a threshold.
If you would like the program to ask each time, set threshold as -1.
Else, set as an integer between 0 and 765.
            """)
        query = input("Set default threshold> ")
        if (int(query) >= -1) and (int(query) <= 765):
            config['CONTROL']['defaultThreshold'] = query
            with open('settings.ini', 'w') as cfile:
                config.write(cfile)
            print("Set new setting of: ",query)
        else:
            print("not an acceptable value. no value set.")

    if userInput in ['settings_step']:
        print("""
sets default step value along the spectral trace (and thus resolution of
resulting intensity plot). default is 1 pixel-equivalence.
            """)
        query = input("Set step value> ")
        if float(query) > 0:
            config['CONTROL']['r'] = query
            with open('settings.ini', 'w') as cfile:
                config.write(cfile)
            print("Set new setting of: ", query)
        else:
            print("value must be greater than zero. no value set.")

    if userInput in ["settings_stop"]:
        print("""
If crop is cutting off data in a certain direction, use the TB (top to bottom)
BT, RL, or LR settings to cut off the auto-crop at a certain column. The default
is -1 for all values.
            """)
        query = input("value to set (integer)?> ")
        value = query
        print("Answer using 'tb','bt','rl', or 'lr'.")
        query = input("Set which? T to B, B to T, R to L, L to R?> ")
        if query in ['tb']:
            config['CONTROL']['autoStopTB'] = value
            with open('settings.ini', 'w') as cfile:
                config.write(cfile)
            print("Set new setting of: ",value, "to ", query)
        if query in ['bt']:
            config['CONTROL']['autoStopBT'] = value
            with open('settings.ini', 'w') as cfile:
                config.write(cfile)
            print("Set new setting of: ",value, "to ", query)
        if query in ['rl']:
            config['CONTROL']['autoStopRL'] = value
            with open('settings.ini', 'w') as cfile:
                config.write(cfile)
            print("Set new setting of: ",value, "to ", query)
        if query in ['lr']:
            config['CONTROL']['autoStopLR'] = value
            with open('settings.ini', 'w') as cfile:
                config.write(cfile)
            print("Set new setting of: ",value, "to ", query)
        else:
            print("not an acceptable value. no value set.")

    if userInput in ['view_settings']:
        print("Current settings:")
        print("default threshold: ", config['CONTROL']['defaultThreshold'])
        print("autoIntensity: ", config['CONTROL']['autoIntensity'])
        print("autoStopTB:", config['CONTROL']['autoStopTB'])
        print("autoStopBT:", config['CONTROL']['autoStopBT'])
        print("autoStopRL:", config['CONTROL']['autoStopRL'])
        print("autoStopLR:", config['CONTROL']['autoStopLR'])
        print("step:", config['CONTROL']['r'])

    #PROGRAM COMMANDS NEXT
    if userInput in prgmCommands:
        print("""
We need a file. Place it in the same directory as this script and give the name.
            """)
        path = input("enter filename> ")
        print("converting. please wait...")
        img = Image.open(path)
        dataArray = to.converter(path)
        
        if defThresh in ['-1']:
            print("""
Your answer to the following depends for all commands except 'pixel_d'.
What threshold would you like to use as differentiator?
                """)
            thresh = input("enter threshold> ")
            threshI = int(thresh)
        else:
            threshI = int(defThresh)

        if userInput in ["intensity_saa", "saa"]:
            print("working on intensity_saa. please wait...")
            regTup = st.regression(img)
            intensity = st.intensitySAAN(img,dataArray,regTup, threshI,step)
            to.plotIntensity(intensity)

        if userInput in ["intensity_n", "n"]:
            print("working on intensity_n. please wait...")
            regTup = st.regression(img)
            intensity = st.intensityN(img,dataArray,regTup, threshI,step)
            to.plotIntensity(intensity)

        if userInput in ["image_regression", "imgreg"]:
            print("working on image_regression. please wait...")
            regTup = st.regression(img)
            to.plotRegression(regTup)

        if userInput in ["pixel_d", "pd"]:
            print("working on pixel_distribution. please wait...")
            to.pixelDistribution(dataArray)

        if userInput in ["crop"]:
            print("working on crop. please wait...")
            cropped = st.crop(img, threshI, TB, BT, RL, LR)
            filename = input("filename for cropped? DO NOT ADD EXTENSION> ")
            to.restorer(cropped, filename)
            print("file has been created at: ", filename + ".tiff")

        if userInput in ["show_threshold"]:
            print("working on show_threshold")
            to.showThreshold(dataArray, threshI)

        if userInput in ["show_regression"]:
            print("working on show_regression")
            regTup = st.regression(img)
            to.showRegression(img,regTup)

        if userInput in ["show_walks"]:
            print("working on show_walks")
            regTup = st.regression(img)
            to.showWalks(img,regTup,step)

        #rehashing of command lists
        print("""
Type 'q', 'quit', or 'exit' to leave this program. Alternately, you may use
ctrl-c to force-interrupt at any time. Type 'help' for sample workflow,
'commands' for a list of functions and commands, and 'about' for more info.
            """)

    elif userInput in ["q", "quit", "exit"]:
        break

    elif userInput in ["jellyfish"]:
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
        print(":)")
