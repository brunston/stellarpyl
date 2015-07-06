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

while True:
    print("q to exit")
    print("0 for actual file, 1 for sample")
    print("2 for regression test, 3 for rotate test")
    blah = input("> ")
    if blah == "0":
        file = 'IMG_2860.tif'
        fileArray = st.converter(file)
        cropped = st.crop(fileArray)
        st.restorer(cropped)
        distribution = st.pixelDistribution(cropped)
        intensity = st.intensity(cropped)
        st.plotGraph(intensity)
        # writeLogToFile(fileArray,'log.log')
    if blah == "1":
        test = de.testArray() #will print out the array generated.
        # sums = st.sumGenerator(test)
        # print(sums)
        cropped = st.crop(test)
        print("duplicate returned from crop():\n", cropped)

    if blah == "2":
        testRotate = de.testRotate()
        print("testRotate:\n", testRotate)
        st.regression(testRotate, 0) #test matrix threshold is 0
        

    if blah == "3":
        testArray = de.testArray()
        testRotate = de.testRotate()
        print("testRotate:\n",testRotate)
        rotated = st.rotate(testRotate,30.0)
        print("rotated:\n",rotated)
    if blah in ("q", "quit", "exit"):
        break
