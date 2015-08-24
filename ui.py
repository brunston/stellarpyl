# -*- coding: utf-8 -*-
"""
stellarPYL - python stellar spectra processing software
Copyright (c) 2015 Brunston Poon
@file: ui
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
Full license in LICENCE.txt
"""

#IMPORT IMPORT IMPORT IMPORT IMPORT IMPORT IMPORT IMPORT IMPORT IMPORT IMPORT
#Let's make sure that the user has all the dependencies installed and that
#they are running the correct version of Python
import sys
import configparser
import time

toggle = True
version = sys.version_info[0]

if version != 3:
    print("""
Please upgrade to Python3, preferably 3.4.* or greater, before continuing""")
    toggle = False
    sys.exit()

try:
    import numpy as np
    from PIL import Image
    from matplotlib import pyplot
except ImportError:
    print("""
numpy, PIL, and/or matplotlib are not installed.
Please install before continuing.""")
    toggle = False
    sys.exit()

#import the rest
import stellar as st
import tools as to
import text as txt
#END IMPORT END IMPORT END IMPORT END IMPORT END IMPORT END IMPORT END IMPORT


if toggle == True:
    config = configparser.ConfigParser()
    config.read('settings.ini')
    firstrun = config['CONTROL']['firstrun']
    txt.welcome()

    if firstrun in ["yes"]:
        txt.firstrun()
        time.sleep(15)
        txt.commands()
        config['CONTROL']['firstrun'] = "no"
        with open('settings.ini', 'w') as cfile:
                config.write(cfile)

while toggle == True:
    #update settings
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

    prgmCommands = ("pixel_d", "image_regression", \
                    "intensity_n", "intensity_saa", \
                    "pd", "imgreg", "saa", "n", "crop", "show_threshold",\
                    "show_regression", "show_walks", "dev_cgrowth")

    userInput = input("enter command> ")

    #TEXT COMMANDS NEXT
    if userInput in ["about"]:
        txt.about()
    if userInput in ["help"]:
        txt.help()
    if userInput in ["commands"]:
        txt.commands()
    if userInput in ["licence", "license"]:
        txt.licence()
    
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
            if showthresh == "yes":
                to.showThreshold(dataArray, threshI)
            timePause0s = time.time()
            print("working on crop. please wait...")
            cropped = st.cropN(img, threshI, top, bottom, left, right, margin)
            to.restorer(cropped, 'cropped')
            print("cropped image saved to cropped.tiff")
            croppedimg = Image.open('cropped.tiff')
            print("converting cropped image. please wait...")
            dataArray = to.converter('cropped.tiff')
            regTup = st.regression(croppedimg)
            timePause1 = time.time()
            to.showRegression(croppedimg,regTup)
            timePause1s = time.time()
            if autoIntensity in ['saa']:
                print("working on intensity_saa. please wait...")
                intensity = st.intensitySAAN(croppedimg,dataArray,regTup,\
                                             threshI,step)
                timePause2 = time.time()
                to.plotIntensity(intensity)
                timePause2s = time.time()
            if autoIntensity in ['saanb']:
                print("working on intensity_saanb. please wait...")
                sys.stdout = open("foo.log", "w")
                intensity = st.intensitySAANB(croppedimg,dataArray,regTup,\
                                             threshI,step,10)
                timePause2 = time.time()
                to.plotIntensity(intensity)
                timePause2s = time.time()
                sys.stdout = sys.__stdout__
            if autoIntensity in ['n']:
                print("working on intensity_n. please wait...")
                intensity = st.intensityN(croppedimg,dataArray,regTup,\
                                          threshI,step)
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
        if query in ['saa', 'n', 'saanb']:
            config['CONTROL']['autointensity'] = query
            with open('settings.ini', 'w') as cfile:
                config.write(cfile)
            print("Set new setting of: ",query)
        else:
            print("not an acceptable value. no value set.")

    if userInput in ["settings_threshold"]:
        print("""
sets a default threshold for any function of this program requiring a threshold.
If you would like the program to ask each time, set threshold as -1.
Else, set as an integer between 0 and 765. Defaults to -1 (ask every time)
            """)
        query = input("Set default threshold> ")
        if (int(query) >= -1) and (int(query) <= 765):
            config['CONTROL']['defaultthreshold'] = query
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

    if userInput in ["settings_cropoverride"]:
        print("""
sets manual overrides for automatic cropping on the top, bottom, and sides
of an image. The default value is -1 (which is equivalent to no override)
for all values.
            """)
        query = input("value to set (integer)?> ")
        value = query
        print("Answer using 'top','bottom','left', or 'right'.")
        query = input("Set override for which side?> ")
        if query in ['top']:
            config['CONTROL']['manualtop'] = value
            with open('settings.ini', 'w') as cfile:
                config.write(cfile)
            print("Set new setting of: ",value, "to ", query)
        elif query in ['bottom']:
            config['CONTROL']['manualbot'] = value
            with open('settings.ini', 'w') as cfile:
                config.write(cfile)
            print("Set new setting of: ",value, "to ", query)
        elif query in ['left']:
            config['CONTROL']['manualleft'] = value
            with open('settings.ini', 'w') as cfile:
                config.write(cfile)
            print("Set new setting of: ",value, "to ", query)
        elif query in ['right']:
            config['CONTROL']['manualright'] = value
            with open('settings.ini', 'w') as cfile:
                config.write(cfile)
            print("Set new setting of: ",value, "to ", query)
        else:
            print("not an understood side name. no value set.")

    if userInput in ['settings_verbose']:
        print("""
sets verbose printing of debug statements. default is 'no'
            """)
        query = input("Set verbose 'yes'/'no'> ")
        if query in ['yes', 'no']:
            config['CONTROL']['verbose'] = query
            with open('settings.ini', 'w') as cfile:
                config.write(cfile)
            print("Set new setting of: ", query)
        else:
            print("not an acceptable value. no value set.")

    if userInput in ['settings_showthreshold']:
        print("""
showThreshold takes a while to run. Set to 'no' for a faster autoProcess
run time. Default is 'yes'
            """)
        query = input("Set verbose 'yes'/'no'> ")
        if query in ['yes', 'no']:
            config['CONTROL']['showthresh'] = query
            with open('settings.ini', 'w') as cfile:
                config.write(cfile)
            print("Set new setting of: ", query)
        else:
            print("not an acceptable value. no value set.")

    if userInput in ['settings_margin']:
        print("""
sets margin for cropping. default margin is 5 pixels
            """)
        query = input("Set margin (integer)> ")
        if int(query) >= 0:
            config['CONTROL']['margin'] = query
            with open('settings.ini', 'w') as cfile:
                config.write(cfile)
            print("Set new setting of: ", query)
        else:
            print("not an acceptable value. no value set.")

    if userInput in ['view_settings']:
        txt.viewSettings(config)

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
            intensity = st.intensitySAAN(img,dataArray,regTup,threshI,step)
            to.plotIntensity(intensity)

        if userInput in ["intensity_n", "n"]:
            print("working on intensity_n. please wait...")
            regTup = st.regression(img)
            intensity = st.intensityN(img,dataArray,regTup,threshI,step)
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
            cropped = st.cropN(img, threshI, top, bottom, left, right, margin)
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
            to.showWalks(img,regTup,r=step)

        if userInput in ["dev_cgrowth"]:
            print("devmode: curve of growth")
            regTup = st.regression(img)
            intensity = st.intensitySAAN(img,dataArray,regTup,threshI,step)
        #rehashing of command lists
        txt.rehash()

    elif userInput in ["q", "quit", "exit"]:
        sys.exit()

    elif userInput in ["jellyfish"]:
        txt.jellyfish()

    else:
        print("Please enter a command.")