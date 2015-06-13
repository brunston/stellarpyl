# -*- coding: utf-8 -*-
"""
stellarPY
@file: tests
@author: Brunston Poon
@org: UH-IFA / SPS
"""

from stellar import *
from debug import *
import numpy as np

file = 'IMG_2860.tif'

fileArray = converter(file)
writeLogToFile(fileArray)

def testArray(nparray):
    """
    This will create a test array with the same dimensions as inputted nparray
    """
    returner = np.zeros_like(nparray)
    #need to put random non-zero values in certain places so that we can make
    #sure that the crop loop is terminating where it should
    return returner