# -*- coding: utf-8 -*-
"""
stellarPY
@file: debug
@author: Brunston Poon
@org: UH-IFA / SPS
"""

import numpy as np
from PIL import Image
import stellar as st

def writeLogToFile(nparray,logname):
    """
    Writes a log to a file with the contents of a numpy array nparray
    """

    with open(logname, 'w') as file:
        for i in range(len(nparray)-1):
            file.write(str(nparray[i]))

    print("Wrote log to", logname)
    #this function does not return anything, only writing a file

def testZeros(nparray):
    """
    testZeros will create a zeroed test array with the same dimensions as
    inputted nparray
    """
    returner = np.zeros_like(nparray)
    return returner

def testArray():
    """
    testArray returns an ndarray of shape [3,50,3] to emulate a small version
    of the tif file ndarray but in a very controlled manner so that testing
    the crop function can be done smoothly.
    """
    dataNone = [0,0,0] #this simulates an empty pixel value
    dataLow = [1,0,2] #values of these pixels go from 0 to 255
    dataHigh = [50,43,29] #this is our test 'high' value
    emptyRow = []
    for i in range(50): #creating a 50-pixel wide row
        emptyRow.append(dataNone)
    semiFilled = []
    for j in range(10): #ten pixels of empty
        semiFilled.append(dataNone)
    for k in range(10): #ten pixels of low
        semiFilled.append(dataLow)
    for l in range(20): #20 pixels of high
        semiFilled.append(dataHigh)
    for m in range(10): #10 pixels of empty
        semiFilled.append(dataNone)
    retArray = [emptyRow, emptyRow, semiFilled, emptyRow, emptyRow]
    retNP = np.array(retArray, dtype=np.uint8)
    print("array generated:\n", retNP)
    return retNP

def joshArray0():
    dataNone = [0,0,0] #this simulates an empty pixel value
    dataLow = [1,0,2] #values of these pixels go from 0 to 255
    dataHigh = [50,43,29] #this is our test 'high' value
    emptyRow = []
    for i in range(50): #creating a 50-pixel wide row
        emptyRow.append(dataNone)
    retArray = [emptyRow]
    retNP = np.array(retArray, dtype = np.uint8)
    print("josh array empty 1 row:\n", retNP)
    return retNP

def joshArray01():
    dataNone = [0,0,0] #this simulates an empty pixel value
    dataLow = [1,0,2] #values of these pixels go from 0 to 255
    dataHigh = [50,43,29] #this is our test 'high' value
    emptyRow = []
    for i in range(50): #creating a 50-pixel wide row
        emptyRow.append(dataNone)
    semiFilled = []
    for j in range(10): #ten pixels of empty
        semiFilled.append(dataNone)
    for k in range(10): #ten pixels of low
        semiFilled.append(dataLow)
    for l in range(20): #20 pixels of high
        semiFilled.append(dataHigh)
    for m in range(10): #10 pixels of empty
        semiFilled.append(dataNone)
    retArray = [emptyRow, semiFilled]
    print("josh array 1 empty 1 filled")
    retNP = np.array(retArray, dtype=np.uint8)
    return retNP

def joshArray001():
    dataNone = [0,0,0] #this simulates an empty pixel value
    dataLow = [1,0,2] #values of these pixels go from 0 to 255
    dataHigh = [50,43,29] #this is our test 'high' value
    emptyRow = []
    for i in range(50): #creating a 50-pixel wide row
        emptyRow.append(dataNone)
    semiFilled = []
    for j in range(10): #ten pixels of empty
        semiFilled.append(dataNone)
    for k in range(10): #ten pixels of low
        semiFilled.append(dataLow)
    for l in range(20): #20 pixels of high
        semiFilled.append(dataHigh)
    for m in range(10): #10 pixels of empty
        semiFilled.append(dataNone)
    retArray = [emptyRow, emptyRow, semiFilled]
    print("josh array 2 empty 1 filled")
    retNP = np.array(retArray, dtype=np.uint8)
    return retNP

def joshArray0010():
    dataNone = [0,0,0] #this simulates an empty pixel value
    dataLow = [1,0,2] #values of these pixels go from 0 to 255
    dataHigh = [50,43,29] #this is our test 'high' value
    emptyRow = []
    for i in range(50): #creating a 50-pixel wide row
        emptyRow.append(dataNone)
    semiFilled = []
    for j in range(2): #two pixels of empty
        semiFilled.append(dataNone)
    for k in range(10): #ten pixels of low
        semiFilled.append(dataLow)
    for l in range(20): #20 pixels of high
        semiFilled.append(dataHigh)
    for m in range(18): #10 pixels of empty
        semiFilled.append(dataNone)
    retArray = [emptyRow, emptyRow, semiFilled, emptyRow]
    print("josh array 2 empty 1 filled 1 empty")
    retNP = np.array(retArray, dtype=np.uint8)
    return retNP

def joshArray00():
    dataNone = [0,0,0] #this simulates an empty pixel value
    dataLow = [1,0,2] #values of these pixels go from 0 to 255
    dataHigh = [50,43,29] #this is our test 'high' value
    emptyRow = []
    for i in range(50): #creating a 50-pixel wide row
        emptyRow.append(dataNone)
    semiFilled = []
    for j in range(10): #ten pixels of empty
        semiFilled.append(dataNone)
    for k in range(10): #ten pixels of low
        semiFilled.append(dataLow)
    for l in range(20): #20 pixels of high
        semiFilled.append(dataHigh)
    for m in range(10): #10 pixels of empty
        semiFilled.append(dataNone)
    retArray = [emptyRow, semiFilled]
    print("josh array 2 empty")
    retNP = np.array(retArray, dtype=np.uint8)
    return retNP
