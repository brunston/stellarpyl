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

def simpleArray():
    """
    Returns the hand-built simple array requested for simple testing of shape
    """
    dataNone = [0,0,0] #this simulates an empty pixel value
    dataLow = [1,0,2] #values of these pixels go from 0 to 255
    emptyRow = []
    r,rg,g,gb,b = [40,20,20], [40,30,20], [20,40,20], [20,40,30], [20,20,40]
    for i in range(20): #creating a 20-pixel wide row
        emptyRow.append(dataNone)
    kinda = []
    for j in range(5): kinda.append(dataNone)
    for k in range(10): kinda.append(dataLow)
    for l in range(5): kinda.append(dataNone)
    row1, row2, row3, row4, row5 = [], [], [], [], []
    for m in range(2): row1.append(dataNone)
    for n in range(2): row1.append(r)
    for o in range(18): row1.append(dataNone)
    for p in range(4): row2.append(dataNone)
    for q in range(2): row2.append(rg)
    for r in range(16): row2.append(dataNone)
    for s in range(6): row3.append(dataNone)
    for t in range(2): row3.append(g)
    for u in range(14): row3.append(dataNone)
    for v in range(6): row4.append(dataNone)
    for w in range(2): row4.append(gb)
    for x in range(12): row4.append(dataNone)
    for y in range(8): row5.append(dataNone)
    for z in range(2): row5.append(b)
    for a in range(10): row5.append(dataNone)
    print("kinda",kinda)
    #retArray = [emptyRow, kinda, row1, row2, row3, row4, row5, emptyRow, emptyRow]
    retArray = []
    retArray.append(emptyRow)
    retArray.append(kinda)
    retArray.append(row1)
    retArray.append(row2)
    retArray.append(row3)
    retArray.append(row4)
    retArray.append(row5)
    retArray.append(emptyRow)
    retArray.append(emptyRow)
    retNP = np.asarray(retArray)
    print("array generated:\n", retNP)
    return retNP

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
    kinda = []
    for n in range(10):
        kinda.append(dataNone)
    for o in range(20):
        kinda.append(dataLow)
    for p in range(20):
        kinda.append(dataNone)
    print("kinda", kinda)
    retArray = [emptyRow, kinda, semiFilled, emptyRow, emptyRow]
    retNP = np.array(retArray, dtype=np.uint8)
    print("array generated:\n", retNP)
    return retNP

def testRotate():
    """
    returns a 2d ndarray which will test the rotate() function in stellar
    """
    array = np.array([[0,0,0,0,0,0],
             [0,0,0,0,0,9,10],
             [0,0,0,6,7,8,0],
             [0,3,4,5,0,0,0],
             [1,2,0,0,0,0,0]])
    return array

def testZeros(nparray):
    """
    testZeros will create a zeroed test array with the same dimensions as
    inputted nparray
    """
    returner = np.zeros_like(nparray)
    return returner

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
