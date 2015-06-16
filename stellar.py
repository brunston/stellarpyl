# -*- coding: utf-8 -*-
"""
stellarPY
@file: primary
@author: Brunston Poon
@org: UH-IFA / SPS
"""

import numpy as np
from PIL import Image

def converter(imageToConvert):
    """
    Converts image given in filepath format as tif to a numpy array and returns
    """
    #note- for some reason, Lightroom-cropped tif files do not play nice.
    #Use original files.

    image = Image.open(imageToConvert)
    imageArray = np.array(image)

    #troubleshooting statements
    print("ndarray imageArray:\n", imageArray)
    print("imageArray shape:", imageArray.shape)
    print("imageArray dtype:", imageArray.dtype)

    return imageArray

def crop(image): #Working from previous code now contained in oldcrop
    """
    Crops an image img based on the number of empty pixels [0,0,0]
    Crops top-to-bottom, right-to-left, bottom-to-top, and then left-to-right
    based on the way that the current set of data has been collected.
    """
    """
    The importation of the tif using PIL works like this: Each row in the
    array array[i] is a list of lists. Each list in the list (array[i][j]) is
    a list of 3 values where each value refers to the RGB value (HAVE TO FIND
    OUT IF IT IS IN THAT ORDER).
    """
    incrementer = False
    duplicate = image
    for j in range(len(duplicate)-1): #goes by line
        counterPerRow = 0
        #what is up with the first for loop being -1
        #and the second just left
        for i in range(len(duplicate[j])): #goes py pixel in line
            if np.array_equal(duplicate[j][i], np.array([0,0,0])):
                #adds to counter if pixel is empty
                counterPerRow = counterPerRow + 1
                if counterPerRow == len(duplicate[0]):
                    #if whole row is empty, delete the row in question
                    duplicate = np.delete(duplicate, j, 0)
                    print("for loopcount:", i)
                    print("counterPerRow value:", counterPerRow)
            #TODO something interesting to think about -- could it be that
            #noise from the detector is gonna prevent a row of perfect zeros?
    return duplicate
#TODO write a function which will determine the greatest singluar value
#in our array so that we can see how much tolerance we have of deleting
#1s, 2s, 3s etc.
