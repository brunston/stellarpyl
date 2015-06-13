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
    print(imageArray)
    print(imageArray.shape)
    print(imageArray.dtype)
    
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
    counterPerRow = 0
    duplicate = image
    for i in range(len(duplicate[0][i])-1):
        if duplicate[0][i] == [0,0,0]:
            duplicate = np.delete(duplicate, 0, 0)
            #TODO something interesting to think about -- could it be that
            #noise from the detector is going to prevent a row of perfect zeros?

#TODO write a function which will determine the greatest singluar value
#in our array so that we can see how much tolerance we have of deleting
#1s, 2s, 3s etc.

            
def oldcrop(image):
    """
    OLD OLD CODE CODE DO NOT USE
    """
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
    counterPerRow = 0
    duplicate = image
    while incrementer == False:
        for i in range(len(image)-1): #per row
            for j in range(len(image[i])-1): #per pixel
                if image[i][j] == [0,0,0]:
                    counterPerRow = counterPerRow + 1
            if counterPerRow == len(image[i]):
                #delete duplicate top row.
                #how to do this without messing up the count
                #always test the top row? that could do it, instaed of using
                #a metric blah of for loopings.
                pass