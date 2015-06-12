# -*- coding: utf-8 -*-
"""
stellarPY
@file: debug
@author: Brunston Poon
@org: UH-IFA / SPS
"""

import numpy as np
from stellar import *

def writeLogToFile(nparray):
    """
    Writes a log to a file with the contents of a numpy array nparray
    """
    
    with open('log.log', 'w') as file:
        for i in range(len(nparray)-1):
            file.write(str(nparray[i]))
            
    #this function does not return anything, only writing a file