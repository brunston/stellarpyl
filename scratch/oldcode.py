# -*- coding: utf-8 -*-
"""
stellarPY
@file: oldcode
@author: Brunston Poon
@org: UH-IFA / SPS
"""
from scipy import ndimage #for rotate

#where old code goes to. This file is a small farm up north
# path = '127.tiff'
# img = Image.open(path)
# regTup = st.regression(img)
# dataArray = st.converter(path)
# to.plotRegression(regTup)
# intensity = st.intensityN(img,dataArray,regTup, 127)
# to.plotIntensity(intensity)
def intensitySAANB(img, data, reg, threshold=127, r=1, twidth=10):
    """
    intensitySAANB is the fourth iteration of the intensity function which aims
    to deal with the plotting of regressed non-orthogonal spectra given in
    an open image img, the pixel data in data, and a regArray generated
    using regression().
    SAA - spatial antialiasing; NB - new, box method
    Returns a dictionary where key is x value and y
    value is intensity.
    r is the step rate along the spectral trace (default to size of one pixel)
    t is the width of the trace on each side of the line y = mx + c
    so the total will be double
    """
    
    lowerx, lowery, upperx, uppery = img.getbbox()
    m, c = reg[0:2]
    n = -1 / m
    #background subtraction median calculation
    back = backMedian(img, threshold)
    if v=='yes': print("backMedian:", back)
    print("running intensitySAAN")
    intensities = {} #this is a dictionary.
    angle = np.arctan(m)
    step = math.sqrt((r**2) / (1 + m**2))

    for xpixel in np.linspace(lowerx, upperx,num=math.ceil((upperx/step)+1)):
        ypixel = m * xpixel + c
        for newx in np.arange(lowerx, upperx - 1, 0.1):
            newy = n * (newx - xpixel) + ypixel #point-slope, add ypixel ea.side
            #We want to add spectral trace width functionality
            if (newy > (ypixel-twidth)) or (newy < (ypixel+twidth)):
                #anti-aliasing implementation http://is.gd/dnj08y
                foo = 1
                for newxRounded in \
                np.linspace(math.floor(newx), math.ceil(newx+r),foo):
                    for newyRounded in (math.floor(newy), math.ceil(newy)):
                        #we need to be sure that the rounded point is in our img
                        if (newyRounded > lowery) and (newyRounded < uppery)\
                            and (newxRounded>lowerx) and (newxRounded < upperx):
                            percentNewX = 1 - abs(newx - newxRounded)
                            percentNewY = 1 - abs(newy - newyRounded)
                            percent = percentNewX * percentNewY
                            #get antialiased intensity from pixel
                            pixel = img.getpixel((newxRounded,newyRounded))
                            if v=='yes': print("using pixel {0},{1}".format(\
                                                newxRounded,newyRounded))
                            newValue = percent * (pixel[0]+pixel[1]+pixel[2])
                            if v=='yes': print("value being added:",newValue)
                            #to ensure we don't reset a value instead of adding:
                            if xpixel in intensities:
                                intensities[xpixel] = \
                                                    intensities[xpixel] + \
                                                    newValue
                            else:
                                intensities[xpixel] = newValue
                            intensities[xpixel] -= percent * back
        to.pbar(xpixel/upperx) #progress bar

    if v=='yes': print("intensities:", intensities)
    return intensities

def notintensitySAANB(img, data, reg, threshold=127, r=1,twidth=10):
    """
    intensitySAANB is the fourth iteration of the intensity function which aims
    to deal with the plotting of regressed non-orthogonal spectra given in
    an open image img, the pixel data in data, and a regArray generated
    using regression().
    SAA - spatial antialiasing; NB - new, box method
    Returns a dictionary where key is x value and y
    value is intensity.
    r is the step rate along the spectral trace (default to size of one pixel)
    """
    
    lowerx, lowery, upperx, uppery = img.getbbox()
    m, c = reg[0:2]
    n = -1 / m
    #background subtraction median calculation
    back = backMedian(img, threshold)
    if v=='yes': print("backMedian:", back)
    print("running intensitySAAN")
    intensities = {} #this is a dictionary.
    step = math.sqrt((r**2) / (1 + m**2))
    #generate the coordinate arrays for our image
    xArr = np.arange(upperx+1)
    yArr = np.arange(uppery+1)
    lineM = np.multiply(m, xArr)
    lineM = np.add(c, lineM)
    r = 0.5 * r
    for pointX in np.linspace(lowerx, upperx,num=math.ceil((upperx/step)+1)):
        #pointY = n * (pointX - 
        for y in range(uppery+1):

            pointIndices = np.where((yArr[y] <= (m * xArr + twidth)) &\
                                    (yArr[y] >= (m * xArr - twidth)) &\
                                    (xArr[y] <= (n * xArr + r)) &\
                                    (xArr[y] >= (n * xArr - r)))
            print("pointIndices for {0}: ".format(y), pointIndices)
            for point in pointIndices:
                if pointX in intensities:
                    intensities[pointX] = intensities[pointX] + point
                else:
                    intensities[pointX] = point
                #todo intensities[pointX] -= percent * back DEAL WITH THIS

        to.pbar(pointX/upperx) #progress bar
    if v=='yes': print("intensities:", intensities)
    return intensities

def showWalks(img, reg, r=1):
    """
    shows walking lines overlayed on the original (cropped) image.
    """
    print("running showRegression")
    lowerx, lowery, upperx, uppery = img.getbbox()
    m, c, x, y = reg
    n = -1/m
    plt.figure(2)
    plt.imshow(img)
    step = math.sqrt((r**2) / (1+m**2))
    counter = 0
    for xpixel in np.linspace(lowerx, upperx, num = math.ceil((upperx/step)+1)):
        ypixel = m * xpixel + c
        if (counter % 2) == 1:
            plt.plot(x, n * (x - xpixel) + ypixel,'r',linestyle='-')
        else:
            plt.plot(x, n * (x - xpixel) + ypixel,'b',linestyle='-')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.axis('off')
    plt.savefig('walks.png', bbox_inches='tight')
    plt.show()
    print("figure saved to walks.png")
    return None
#wrong stepping method and also still has logging
def intensitySAA(img, data, reg, threshold=127):
    """
    intensitySAA is the third iteration of the intensity function which aims
    to deal with the plotting of regressed non-orthogonal spectra given in
    an open image img, the pixel data in data, and a regArray generated
    using regression(). Returns a dictionary where key is x value and y
    value is intensity.
    """
    #logging start debug
    #f = open('log_intensity.log', 'w')
    #sys.stdout = f
    #np.set_printoptions(threshold=np.nan)
    #//logging start

    lowerx, lowery, upperx, uppery = img.getbbox()
    m, c = reg[0:2]
    n = -1 / m
    #background subtraction median calculation
    back = backMedian(img, threshold)

    intensities = {} #this is a dictionary.
    for xpixel in range(lowerx, upperx):
        ypixel = m * xpixel + c
        for newx in np.arange(lowerx, upperx - 1, 0.1): #I missed the -1 in iQ
            #newx = modpixel from iQ, newy = crossDispersion from iQ
            newy = n * (newx - xpixel) + ypixel #point-slope, add ypixel ea.side
            if (newy > lowery) and (newy < uppery):
                #anti-aliasing implementation http://is.gd/dnj08y
                for newxRounded in (math.floor(newx), math.ceil(newx)):
                    for newyRounded in (math.floor(newy), math.ceil(newy)):
                        #we need to be sure that the rounded point is in our img
                        if (newyRounded > lowery) and (newyRounded < uppery):
                            percentNewX = 1 - abs(newx - newxRounded)
                            percentNewY = 1 - abs(newy - newyRounded)
                            percent = percentNewX * percentNewY
                            #get antialiased intensity from pixel
                            pixel = img.getpixel((newxRounded,newyRounded))
                            newValue = percent * (pixel[0]+pixel[1]+pixel[2])
                            #to ensure we don't reset a value instead of adding:
                            if xpixel in intensities:
                                intensities[xpixel] = \
                                                    intensities[xpixel] + \
                                                    newValue
                            else:
                                intensities[xpixel] = newValue
                            intensities[xpixel] -= percent * back

    #logging end debug
    #sys.stdout = sys.__stdout__
    #np.set_printoptions(threshold=1000)
    #//logging end
    print("median background", backMedian)

    return intensities
    #rewritten for cleaner reading from intensityQ, regression_test.py provided
    #by Scott and Wikipedia article on spatial antialiasing found at
    #http://is.gd/dnj08y or wiki-spatial-antialiasing.pdf

def intensityN(img, data, regArray):
    """
    Creates a 'proper' intensity array for the data given in a numpy array and
    using an open Image given in img. Degree offset is calculated by a
    y = mx + c function as done in regression()
    regArray = [xvals_n, yvals_n, A, m, c]
    """
    f = open('log_intensity.log', 'w')
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

def intensitySAA(img, data, regArray, threshold=127):
    """
    intensitySAA is the third iteration of the intensity function which aims
    to deal with the plotting of regressed non-orthogonal spectra given in
    an open image img, the pixel data in data, and a regArray generated
    using regression(). Returns a dictionary where key is x value and y
    value is intensity.
    """
    #logging start
    f = open('log_intensity.log', 'w')
    sys.stdout = f
    np.set_printoptions(threshold=np.nan)
    #//logging start

    lowerx, lowery, upperx, uppery = img.getbbox()
    m, c = regArray[3], regArray[4]
    n = -1 / m
    #background subtraction
    back = []
    for x in range(lowerx, upperx):
        for y in range(lowery, uppery):
            pixel = img.getpixel((x,y))
            pixelSum = pixel[0]+pixel[1]+pixel[2]
            if pixelSum < threshold:
                back.append(pixelSum)
    backMedian = statistics.median(back)

    intensities = {} #this is a dictionary.
    for xpixel in range(lowerx, upperx):
        ypixel = m * xpixel + c
        for newx in np.arange(lowerx, upperx - 1, 0.1): #I missed the -1 in iQ
            #newx = modpixel from iQ, newy = crossDispersion from iQ
            newy = n * (newx - xpixel) + ypixel #point-slope, add ypixel ea.side
            if (newy > lowery) and (newy < uppery):
                #anti-aliasing implementation from wiki-spatial-antialiasing.pdf
                #section 2 or in http://is.gd/dnj08y
                for newxRounded in (math.floor(newx), math.ceil(newx)):
                    for newyRounded in (math.floor(newy), math.ceil(newy)):
                        #we need to be sure that the rounded point is in our img
                        if (newyRounded > lowery) and (newyRounded < uppery):
                            percentNewX = 1 - abs(newx - newxRounded)
                            percentNewY = 1 - abs(newy - newyRounded)
                            percent = percentNewX * percentNewY
                            #get antialiased intensity from pixel
                            pixel = img.getpixel((newxRounded,newyRounded))
                            newValue = percent * (pixel[0]+pixel[1]+pixel[2])
                            #to ensure we don't reset a value instead of adding:
                            if xpixel in intensities:
                                intensities[xpixel] = \
                                                    intensities[xpixel] + \
                                                    newValue
                            else:
                                intensities[xpixel] = newValue
                            intensities[xpixel] -= percent * (backMedian)
    print("back", back)
    #logging end
    sys.stdout = sys.__stdout__
    np.set_printoptions(threshold=1000)
    #//logging end
    print("median background", backMedian)

    return intensities
    #rewritten for cleaner reading from intensityQ, regression_test.py provided
    #by Scott and Wikipedia article on spatial antialiasing found at
    #http://is.gd/dnj08y or wiki-spatial-antialiasing.pdf

def intensity(data):
    """
    Creates an intensity array for the data given in a numpy array. Also allows
    for the insertion of an absolute response function.
    degreeOffset (float) refers to the offset of the data from the horizontal.
    Counter-clockwise (i.e. 'above horizontal') is positive
    Clockwise (i.e. 'below horizontal') is negative
    """
    intensity = []
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

def rotate(data, angle):
    """
    Rotates an ndarray data which has already gone through the sumGenerator
    process at an angle (float) given.
    """
    #TODO needs work
    return ndimage.interpolation.rotate(data, angle)
#failed attempt at super-encapuslation

def intensitySAA(importer, img, data, regArray, intensities, threshold=127):
    """
    intensitySAA is the third iteration of the intensity function which aims
    to deal with the plotting of regressed non-orthogonal spectra given in
    an open image img, the pixel data in data, and a regArray generated
    using regression(). Returns a dictionary where key is x value and y
    value is intensity.
    """
    xpixel, lowery, uppery, newx, newy, \
    newxRounded, newyRounded, backMedian = importer
    
    if (newyRounded > lowery) and (newyRounded < uppery):
        percentNewX = 1 - abs(newx - newxRounded)
        percentNewY = 1 - abs(newy - newyRounded)
        percent = percentNewX * percentNewY
        #get antialiased intensity from pixel
        pixel = img.getpixel((newxRounded,newyRounded))
        newValue = percent * (pixel[0]+pixel[1]+pixel[2])
        #to ensure we don't reset a value instead of adding:
        if xpixel in intensities:
            intensities[xpixel] = \
                                intensities[xpixel] + \
                                newValue
        else:
            intensities[xpixel] = newValue
            intensities[xpixel] -= percent * (backMedian)

def intensityN(importer, img, data, regArray, intensities, threshold=127):
    """
    Creates a 'proper' intensity array for the data given in a numpy array and
    using an open Image given in img. Degree offset is calculated by a
    y = mx + c function as done in regression()
    regArray = [xvals_n, yvals_n, A, m, c]
    """
    if (newyRounded > lowery) and (newyRounded < uppery):
        pixel = img.getpixel((newxRounded,newyRounded))
        newValue = pixel[0]+pixel[1]+pixel[2]
        #to ensure we don't reset a value instead of adding:
        if xpixel in intensities:
            intensities[xpixel] = \
                                intensities[xpixel] + \
                                newValue
        else:
            intensities[xpixel] = newValue
            intensities[xpixel] -= backMedian

def plotIntensityN(intensityN):
    x = []
    y = []
    for element in intensityN:
        x.append(element[0])
        y.append(element[1])
    plt.figure(1)
    plt.clf() #clears figure
    plt.plot(x, y,'b.',markersize=4)
    plt.title("dispOne")

def intensity(img, data, regArray, itype = 'saa', threshold = 127):
    f = open('log_intensity.log', 'w')
    sys.stdout = f
    np.set_printoptions(threshold=np.nan)
    #//logging start

    lowerx, lowery, upperx, uppery = img.getbbox()
    m, c = regArray[3], regArray[4]
    n = -1 / m
    #background subtraction
    back = []
    for x in range(lowerx, upperx):
        for y in range(lowery, uppery):
            pixel = img.getpixel((x,y))
            pixelSum = pixel[0]+pixel[1]+pixel[2]
            if pixelSum < threshold:
                back.append(pixelSum)
    backMedian = statistics.median(back)

    intensities = {} #this is a dictionary.
    for xpixel in range(lowerx, upperx):
        ypixel = m * xpixel + c
        for newx in np.arange(lowerx, upperx - 1, 0.1): #I missed the -1 in iQ
            #newx = modpixel from iQ, newy = crossDispersion from iQ
            newy = n * (newx - xpixel) + ypixel #point-slope, add ypixel ea.side
            if (newy > lowery) and (newy < uppery):
                #anti-aliasing implementation from wiki-spatial-antialiasing.pdf
                #section 2 or in http://is.gd/dnj08y
                for newxRounded in (math.floor(newx), math.ceil(newx)):
                    for newyRounded in (math.floor(newy), math.ceil(newy)):
                        importer = (xpixel, lowery, uppery, newx, newy, \
                                    newxRounded, newyRounded, backMedian)
                        interpolation( \
                                        itype, \
                                        img, data, regArray, importer, \
                                        intensities, threshold \
                                        )
    print("back", back)
    #logging end
    sys.stdout = sys.__stdout__
    np.set_printoptions(threshold=1000)
    #//logging end
    print("median background", backMedian)

    return intensities
    #rewritten for cleaner reading from intensityQ, regression_test.py provided
    #by Scott and Wikipedia article on spatial antialiasing found at
    #http://is.gd/dnj08y or wiki-spatial-antialiasing.pdf

def interpolation(func, img, data, regArray, importer, intensities, threshold=127):
    """
    Function which executes the interpolation type requested (as string)
    as available in the below dictionary.
    from http://stackoverflow.com/questions/2283210/python-function-pointer
    """

    funcDict = {
        'naive':intensityN,
        'saa':intensitySAA,
    }
    try:
        funcDict[func](importer, img, data, regArray, threshold, intensities)
    except KeyError:
        raise Exception("The interpolation method you called does not exist!")
#end failed attempt

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

#old test toggle code
toggle == False
while toggle == True:
    print("commands (shortnames are first two letters):")
    print("'q', 'quit', 'exit', to exit")
    print("'actual' for actual file, 'sample' for sample")
    print("'regression' for regression test, 'rotate' for rotate test")
    print("'simple' for the simple test")
    blah = input("enter command> ")
    if blah in ("simple","si"): #SIMPLE TEST
        array = de.simpleArray()
        #cropped = st.crop(array, 7)
        #intensity = st.intensity(cropped)
        #st.plotGraph(intensity)
        summed = st.sumGenerator(array)
        regArray = st.regression(summed, 7)
        st.plotRegression(regArray)

    elif blah in ("actual", "ac"): #ACTUAL
        file = 'IMG_2860.tif'
        fileArray = st.converter(file)
        cropped = st.crop(fileArray, 110)
        print("cropped.shape:", cropped.shape)
        #st.restorer(cropped)
        #distribution = st.pixelDistribution(cropped)
        #intensity = st.intensity(cropped)
        #st.plotGraph(intensity)
        # writeLogToFile(fileArray,'log.log')

    elif blah in ("sample", "sa"): #SAMPLE
        test = de.testArray() #will print out the array generated.
        # sums = st.sumGenerator(test)
        # print(sums)
        cropped = st.crop(test)
        print("duplicate returned from crop():\n", cropped)

    elif blah in ("reg", "regression", "re"): #REGRESSION TEST
        testRotate = de.testRotate()
        print("testRotate:\n", testRotate)
        print("testRotate.shape:\n", testRotate.shape)
        regArray = st.regression(testRotate, 0) #test matrix threshold is 0
        st.plotRegression(regArray)

    elif blah in ("rotate", "ro"): #ROTATE TEST
        testRotate = de.testRotate()
        print("testRotate:\n",testRotate)
        rotated = st.rotate(testRotate,30.0)
        print("rotated:\n",rotated)

    elif blah in ("q", "quit", "exit"): break
    else: print("please input a recognized command")


<table border="1" style="width:100%">
  <tr>
    <td>'pixel_d' (short 'pd')</td>
    <td>takes an image and shows the pixel distribution of the\
    image over the intensity of the pixels</td>
  </tr>
  <tr>
    <td>'image_regression' (short 'imgreg')</td>
    <td>takes an image and finds the line which goes\
    through the spectrum in that image</td>
  </tr>
  <tr>
    <td>'intensity_n' (short 'n')</td>
    <td>takes an image of a spectrum and converts it into an\
    intensity plot using the naive method of adding</td>
  </tr>
  <tr>
    <td>'intensity_saa' (short 'saa')</td>
    <td>takes an image of a spectrum and converts it into\
    an intensity plot using spatial anti-aliasing at a sub-sampling rate\
    of one tenth of one pixel</td>
  </tr>
  <tr>
    <td>'crop'</td>
    <td>takes an image and crop it based on your selected threshold.</td>
  </tr>
</table>