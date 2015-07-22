# -*- coding: utf-8 -*-
"""
stellarPY
@file: oldcode
@author: Brunston Poon
@org: UH-IFA / SPS
"""

#where old code goes to. This file is a small farm up north

def intensity(data,degreeOffset=0):
    """
    Creates an intensity array for the data given in a numpy array. Also allows
    for the insertion of an absolute response function.
    degreeOffset (float) refers to the offset of the data from the horizontal.
    Counter-clockwise (i.e. 'above horizontal') is positive
    Clockwise (i.e. 'below horizontal') is negative
    """
    intensity = []
    if degreeOffset == 0: #i.e. we just want to add vertically
        for k in range(len(data[0])): #goes by column
            vertSlice = data[:,k] # a single column k with all rows
            #print("vertSlice:\n", vertSlice)
            runningTotal = 0
            for pixel in vertSlice:
                for color in pixel:
                    runningTotal = color + runningTotal
            intensity.append(runningTotal)
    intensityNP = np.array(intensity)
    return intensityNP

def plotGraph(intensity):
    """
    Plots the intensity array generated and returns None
    """
    x = []
    for i in range(len(intensity)):
        #instead of pixel values as is by simply appending 0,1,2, this portion
        #of the function can be set up to use a wavelength-to-pixel ratio.
        x.append(i*1)
    xNP = np.array(x)
    plt.figure(1)
    plt.clf() #clears figure
    plt.plot(xNP, intensity,'b.',markersize=4)
    plt.title("intensity plot, intensity vs wavelength")
    # plt.xlbl("wavelength (nm)")
    # plt.ylbl("intensity (8-bit pixel addition)")
    return None

def intensityP(img, data, regArray):
    """
    Creates a 'proper' intensity array for the data given in a numpy array and
    using an open Image given in img. Degree offset is calculated by a
    y = mx + c function as done in regression()
    regArray = [xvals_n, yvals_n, A, m, c]
    """
    #logging begin
    f = open('log_intensity.txt', 'w')
    sys.stdout = f
    np.set_printoptions(threshold=np.nan)

    xvals_n, yvals_n = regArray[0], regArray[1]
    A, m, c = regArray[2], regArray[3], regArray[4]
    lowerx, lowery, upperx, uppery = img.getbbox()
    sumArray = []
    for xpixel in range(lowerx, upperx):
        #this loop should run across the image by pixel
        sumPerX = 0
        ypixel = math.floor(m * xpixel + c) #we need to floor this value to get a pixel value
        #ypixelfi = uppery - math.floor(ypixel) #f=floor, i=inverted
        n = -1/m
        modpixel = xpixel
        while True: #this is the loop which side-walks up
            print("- a pixel from modpixel, value: ", modpixel)
            modpixel -= 1
            if (modpixel) >= 0: #b/c -1 is a valid index
                try:
                    print("doing crossDispersion calculations")
                    crossDispersion = math.floor(n * (modpixel - xpixel) + ypixel)
                    #taken from y - y1 = n(x - x1) which becomes
                    #y = n(x - x1) + y1
                    #crossDispersionfi = uppery - math.floor(crossDispersion)
                    print("summing data")
                    sumPerElement = 0
                    for element in data[xpixel][crossDispersion]:
                        sumPerElement += element
                    sumPerX += sumPerElement
                    #doing xpixel because the sum is per xpixel on the line...
                except IndexError:
                    print("reached end of image, breaking")
                    break
            else:
                break
        modpixel = xpixel
        while True: #this is the loop which side-walks down
            modpixel += 1
            print("+ a pixel from modpixel, value: ", modpixel)
            try:
                print("doing crossDispersion calculations")
                crossDispersion = math.floor(n * (modpixel - xpixel) + ypixel)
                #taken from y - y1 = m(x - x1) which becomes
                #y = m(x - x1) + y1
                #crossDispersionfi = uppery - math.floor(crossDispersion)
                print("summing data")
                sumPerElement = 0
                for element in data[xpixel][crossDispersion]:
                    sumPerElement += element
                sumPerX += sumPerElement
            except IndexError:
                print("reached end of image, breaking")
                break
        sumArray.append(sumPerX)
    sumArrayn = np.array(sumArray)
    print("sumArrayn:\n", sumArrayn)

    #logging end
    sys.stdout = sys.__stdout__
    np.set_printoptions(threshold=1000)

    return sumArrayn

def intensityQ(img, data, regArray):
    """
    Creates a 'proper' intensity array for the data given in a numpy array and
    using an open Image given in img. Degree offset is calculated by a
    y = mx + c function as done in regression()
    regArray = [xvals_n, yvals_n, A, m, c]
    """
    f = open('log_intensity.txt', 'w')
    sys.stdout = f
    np.set_printoptions(threshold=np.nan)
    m, c = regArray[3], regArray[4]
    
    lowerx, lowery, upperx, uppery = img.getbbox()
    lineArray = []
    for xpixel in range(lowerx, upperx):
        ypixel = m * xpixel + c
        n = -1/m
        for modpixel in np.arange(lowerx, upperx, 0.1):
            print("+ a pixel from modpixel, value: ", modpixel)
            crossDispersion = n * (modpixel - xpixel) + ypixel
            print("pixel (%.2f,%.2f)" %(modpixel, crossDispersion))
            if (crossDispersion > lowery) and (crossDispersion < uppery):
                lineArray.append([round(modpixel), round(crossDispersion)])
                print("appended pixel successfully")
    lineArrayn = np.array(lineArray)
    sumArray = []
    for element in lineArrayn:
        rgbval = 0
        for rgb in data[element[0]][element[1]]:
            rgbval += rgb
        sumArray.append(rgbval)
    sumArrayn = np.array(sumArray)
    print("sumArrayn:\n", sumArrayn)

    #logging end
    sys.stdout = sys.__stdout__
    np.set_printoptions(threshold=1000)

    return sumArrayn

def plotIntensityQ(intensityQ):
    x = []
    y = []
    for element in intensityQ:
        x.append(element[0])
        y.append(element[1])
    plt.figure(1)
    plt.clf() #clears figure
    plt.plot(x, y,'b.',markersize=4)
    plt.title("dispOne")

#testestestestest
def crop(image):
    #oldcode from before I decided to implement Evan's suggestions and Josh's debugging arrays.
    duplicate = np.copy(image)
    counterPerRow = 0
    for i in range(len(duplicate[0])): #goes by pixel in row
        if np.array_equal(duplicate[0][i], np.array([0,0,0])):
            #adds to counter if pixel is empty
            counterPerRow = counterPerRow + 1
        # else:
        #     print("breaking")
        #     print("duplicate:\n", duplicate)
        #     break
        if counterPerRow == len(duplicate[0]):
            #if whole row is empty, delete the row in question
            duplicate = np.delete(duplicate, 0, 0)
            print("Cropping row 0")
            crop(duplicate)
    print("duplicate right before return:\n", duplicate)
    return duplicate


def crop(image): #Working from previous code now contained in oldcrop
    """
    Crops an image img based on the number of empty pixels [0,0,0]
    Crops top-to-bottom, right-to-left, bottom-to-top, and then left-to-right
    based on the way that the current set of data has been collected.
    """

    duplicate = np.copy(image) #working with NEW ARRAY not REFERENCING OLD!!!!

    #cropping horizontally
    for j in range(len(duplicate)): #goes by row
        counterPerRow = 0
        #what is up with the first for loop being -1
        #and the second just left
        for i in range(len(duplicate[j])): #goes by pixel in row
            if np.array_equal(duplicate[j][i], np.array([0,0,0])):
                #adds to counter if pixel is empty
                counterPerRow = counterPerRow + 1
            if counterPerRow == len(duplicate[0]):
                #if whole row is empty, delete the row in question
                duplicate = np.delete(duplicate, j, 0)
            #TODO something interesting to think about -- could it be that
            #noise from the detector is gonna prevent a row of perfect zeros?

    #cropping vertically
    for k in range(len(duplicate[0])-1): #goes by column
        counterPerColumn = 0
        vertSlice = duplicate[:,k] # a single column k with all rows
        print("vertSlice:\n", vertSlice)
        for element in vertSlice:
            if np.array_equal(element, np.array([0,0,0])):
                counterPerColumn = counterPerColumn + 1
                print("counterPercolumn", counterPerColumn)
        if counterPerColumn == len(vertSlice):
            duplicate = np.delete(duplicate, k, 1)

    #TODO figured out what's going on with crop. right now it is currently
    #deleting right away and so the index of the rows and columns is changing
    #and more importantly the shape of the array changes.
    #Ideas to fix this: instead of creating a copy of the old array and
    #subtracting, create a .size [0,0,0] array and add to it...

    return duplicate
#TODO write a function which will determine the greatest singluar value
#in our array so that we can see how much tolerance we have of deleting
#1s, 2s, 3s etc.

#code from some thing i was working on
def weird():
    while toggleBot == True:
        numRow = len(duplicate)
        a = numRow-1
        counterPerCol = 0
        for i in range(numCol):
            if not np.array_equal(duplicate[a][i], np.array([0,0,0])):
                #adds to counter if iterated pixel is empty
                toggleBot = False
                break
            else:
                counterPerCol += 1
        if counterPerCol == len(duplicate[a][0]):
            #if the entire row of pixels is empty, delete row
            duplicate = np.delete(duplicate, 0, 0)
            print("cropping row:", a)
            print("New duplicate:\n", duplicate)
        # else:
        #     break
    return None #added after transfer to oldcode
