# -*- coding: utf-8 -*-
"""
stellarPY
@file: scratch testing
@author: Brunston Poon
@org: UH-IFA / SPS
"""

import numpy as np
from PIL import Image

import stellar as st
import debug as de

#Playing with numpy ndarray slicing
test = de.testArray()
print("testArray, without modification or selection:\n", test)
print("test[0]:\n",test[0])
print("test[:0]:\n",test[:0])
print("test[:,:15]:\n", test[:,:15])
#test[:,:15] produces all of the pixels in each row up to the 15th column
print("test[:,15]:\n", test[:,15])
#SUCCESS! This will produce the 15th column across all the rows. This is great
#because not only will it work for cropping but it  will also help in adding
#all of the pixel values in the column.

#TIF importation using pillow/PIL
"""
The importation of the tif using PIL works like this: Each row in the
array array[i] is a list of lists. Each list in the list (array[i][j]) is
a list of 3 values where each value refers to the RGB value (HAVE TO FIND
OUT IF IT IS IN THAT ORDER).
"""
