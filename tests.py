# -*- coding: utf-8 -*-
"""
stellarPY
@file: tests
@author: Brunston Poon
@org: UH-IFA / SPS
"""

from stellar import *

#file = 'IMG_2860e.tif'

#converter('IMG_2860e.tif')

image = Image.open('img2860.tif')
imageArray = np.array(image)
print(imageArray)