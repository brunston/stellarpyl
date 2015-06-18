# -*- coding: utf-8 -*-
"""
stellarPY
@file: tests
@author: Brunston Poon
@org: UH-IFA / SPS
"""

import stellar as st
import debug as de
import numpy as np

file = 'IMG_2860.tif'
#
fileArray = st.converter(file)
# writeLogToFile(fileArray,'log.log')
#
test = de.testArray() #will print out the array generated.

cropped = st.crop(test)
print("duplicate returned from crop():\n", cropped)

# de.writeLogToFile(cropped,'cropped.log')

intenseTest = st.intensity(fileArray, 0)
st.plotGraph(intenseTest)
