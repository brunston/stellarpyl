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