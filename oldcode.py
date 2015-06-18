# -*- coding: utf-8 -*-
"""
stellarPY
@file: oldcode
@author: Brunston Poon
@org: UH-IFA / SPS
"""

#where old code goes to. This file is a small farm up north

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
