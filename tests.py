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
writeLogToFile(fileArray,'log.log')

test = testArray()

cropped = crop(test)
print(cropped)

writeLogToFile(cropped,'cropped.log')
