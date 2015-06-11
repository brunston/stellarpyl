# -*- coding: utf-8 -*-
"""
stellarPY
@file: primary
@author: Brunston Poon
@org: UH-IFA / SPS
"""

import numpy as np
from PIL import Image

#pre-cropped tif of Pollux @ 5 second integration, 4000k white balance
#no other modification of data
def converter(imageToConvert):
    """
    Converts image given in filepath format as tif to a numpy array and returns
    """
    image = Image.open(imageToConvert)
    imageArray = np.array(image)
    print(imageArray)
    return imageArray