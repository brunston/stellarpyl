def intensityWHERE(img, data, reg, threshold=127, r=1, twidth=10,spss=0.1):
    """
    code example of using numpy.where() to select and sum subsampled points of an image
    img is 
    """
    m, c = reg[0:2]

    #  generate 2D arrays of X and Y values for subsampled points
    #  need to replace 0,10 and 0,5 with the actual sub-image limits
    #  need to reverse y if you are indexing from bottom left of image
    xLimLow,xLimHigh,xSample = 0.0, 3.5, 0.5
    yLimLow,yLimHigh,ySample = 0.0, 2.5, 0.5
    xVals = np.arange(xLimLow, xLimHigh, xSample)
    yVals = np.arange(yLimHigh, yLimLow, -1.0*ySample)
    xMap = np.ones((len(yVals),len(xVals)))
    yMap = np.ones((len(yVals),len(xVals)))
    for i in range(len(yVals)):
        xMap[i,:] = xMap[i,:] * xVals

    for i in range(len(xVals)):
        yMap[:,i] = yMap[:,i] * yVals

    #  make arrays that have the indices for each point in the original image (e.g. the point 1.3, 2.9 maps onto pixel 1,2)
    xMapi = xMap.astype(int)
    yMapi = yMap.astype(int)

    print(xMap)
    print(xMapi)
    print(yMap)
    print(yMapi)

    #  test image.  Just use multiple of X & Y, to have something where totals will clearly change from left to right and bottom to top
    xSimple = np.arange(xLimLow, xLimHigh,1.0)
    ySimple = np.arange(yLimHigh, yLimLow,-1.0)
    img = np.ones((yLimHigh+1,xLimHigh+1))
    for i in range(np.int(yLimHigh+1)):
        img[i,:] = img[i,:]*xSimple

    for i in range(np.int(xLimHigh+1)):
        img[:,i] = img[:,i]*ySimple

    print(img)


    #  test values of slope and y-intercept for fake data
    #  first check that a nearly 0 slope will scan across the middle of the image.  Then try something at a tilt
    #m,c = 0.01, 1.0
    m,c = 0.5, 0.5

    #  test value of binning width.  Set by user in end case (default 1.)
    w = 0.5
    #  test value of number of pixel-widths to include above and below trace.  Default 4 or 5?
    v = 0.5
    # Calculate vertical offset for bounds ahead and behind point along the trace
    offsetTrace = w * np.sqrt(m**2 + 1) / m
    # Calculate vertical offset for bounds above and below the trace
    offsetVertical = v * np.sqrt(m**2 + 1)

    #print m,c,w,v,offsetTrace,offsetVertical    

    testXsize = xLimHigh
    binWidth = w / np.sqrt(m**2+1)
    #  need to fix calculation of the number of needed bins.  Loop below iterates more times than can store
    pArray = np.zeros(np.ceil((testXsize+1-binWidth/2.0)/binWidth))
    qArray = np.zeros(np.ceil((testXsize+1-binWidth/2.0)/binWidth))
    spec1D = np.zeros(np.ceil((testXsize+1-binWidth/2.0)/binWidth))

    # scan across whole test image, in step size adjusting for slope
    # step in from lower limit by half the bin width
    i = 0
    for p in np.arange(0.0 + binWidth/2.0, testXsize+1, binWidth):
        print("Array:",(testXsize+1-binWidth/2.0)/binWidth)
        # Calculate the corresponding y coordinate to p (called q) on our long axis, from our regression, where y = mx + b.                           
        # (p, q) is a point along the center of our spectrum.                                                                                                         
        q = m * p + c
        #print m,c,p,q
        #
        # Calculate slope and y-intercept for perpendicular line through point p,q
        perp_m = -1 / m
        perp_c = q + p/m
        #print m,c,perp_m,perp_c,p,q
        #
        # Store location of central point for each bin
        pArray[i] = p
        qArray[i] = q
        print(i,p,q)
        #
        #  test for points that fall within bounds
        #  get a 2 x n array of Y,X values for points in the subsampled image that fall within the bounds
        include = np.where((yMap < ((-1.0/m)*xMap + perp_c + offsetTrace)) & (yMap >= ((-1.0/m)*xMap + perp_c - offsetTrace)) & (yMap < (m*xMap + c + offsetVertical)) & (yMap >= (m*xMap + c - offsetVertical)))  
        #
        #  Now get the indices in the original image for those points (e.g., 1.3, 2.9 --> 1, 2)
        # 2 - y indices is a kludge to accommodate my coordinates, which are bottom left start 
        # rather than Python's top left start
        includedValues = img[[2-yMapi[include],xMapi[include]]]
        # 
        spec1D[i] = np.sum(includedValues)
        #
        #  make an array to display to illustrate the selection of points from the original image
        displayArray = np.zeros(xMap.shape)
        displayArray[include] = includedValues
        print(include, yMapi[include], xMapi[include], img[[2-yMapi[include],xMapi[include]]])
        print(displayArray)
        i += 1

    print(pArray, qArray, spec1D)