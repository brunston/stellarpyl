

def intensityWHERE(img, data, reg, threshold=127, r=1, twidth=10,spss=0.1):
    """
    code example of using numpy.where() to select and sum subsampled points of an image
    img is
    """

    #  load an arbitrary image to use as testfile
    import os
    from astropy.io import fits

    files = os.listdir('.')
    hdulist = fits.open(files[8])
    header = hdulist[0].header
    img = hdulist[0].data

    #  select a subset of the image to use, and scale it
    xmin = 0
    xmax= 1000
    ymin = 700
    ymax = 1100

    displayImg = (img[ymin:ymax,xmin:xmax] - np.min(img[ymin:ymax,xmin:xmax]))**(0.25)
    imgplot = plt.imshow(displayImg,zorder=0, extent = [xmin,xmax,ymin,ymax])



    #  generate 2D arrays of X and Y values for subsampled points
    #  need to replace 0,10 and 0,5 with the actual sub-image limits
    #  need to reverse y if you are indexing from bottom left of image
    xLimLow,xLimHigh,xSample = xmin, xmax, 0.25
    yLimLow,yLimHigh,ySample = ymin, ymax, 0.25
    xVals = np.arange(xLimLow, xLimHigh, xSample)
    #  did some testing - when print(ING arrays, python print(s row 0 at the top… but in subarray selection and image display, it starts at lower left.  Therefore, don't need -1.0 * ySample
    # yVals = np.arange(yLimHigh, yLimLow, -1.0*ySample)
    yVals = np.arange(yLimLow, yLimHigh, ySample)
    xVals.shape
    yVals.shape
    xMap = np.ones((len(yVals),len(xVals)))
    yMap = np.ones((len(yVals),len(xVals)))
    xMap.shape
    yMap.shape
    for i in range(len(yVals)):
      xMap[i,:] = xMap[i,:] * xVals

    for i in range(len(xVals)):
      yMap[:,i] = yMap[:,i] * yVals

    imgplot = plt.imshow(xMap,zorder=0, extent = [xmin,xmax,ymin,ymax])
    imgplot = plt.imshow(yMap,zorder=0, extent = [xmin,xmax,ymin,ymax])


    #  make arrays that have the indices for each point in the original image (e.g. the point 1.3, 2.9 maps onto pixel 1,2)
    xMapi = xMap.astype(int)
    yMapi = yMap.astype(int)

    imgplot = plt.imshow(xMapi,zorder=0, extent = [xmin,xmax,ymin,ymax])
    imgplot = plt.imshow(yMapi,zorder=0, extent = [xmin,xmax,ymin,ymax])

    print(xMap)
    print(xMapi)
    print(yMap)
    print(yMapi)

    #  test image.  Just use multiple of X & Y, to have something where totals will clearly change from left to right and bottom to top
    #  NOT USING THIS ANYMORE
    xSimple = np.arange(xLimLow, xLimHigh,1.0)
    ySimple = np.arange(yLimHigh, yLimLow,-1.0)
    img = np.ones((yLimHigh+1,xLimHigh+1))
    for i in range(np.int(yLimHigh+1)):
     img[i,:] = img[i,:]*xSimple

    for i in range(np.int(xLimHigh+1)):
     img[:,i] = img[:,i]*ySimple

    print(img)

    # test image
    subImg = img[ymin:ymax,xmin:xmax]
    displayImg = (subImg - np.min(subImg))**(0.25)
    #imgplot = plt.imshow(displayImg,zorder=0, extent = [xmin,xmax,ymin,ymax])
    plotSetting = 111

    ax1 = plt.subplot(plotSetting)
    ax1.imshow(displayImg,zorder=0, extent = [xmin,xmax,ymin,ymax])
    plt.show()

    #  select a "regression" that passes near something bright
    reg = [0.1,960]
    m, c = reg[0:2]




    #  test values of slope and y-intercept for fake data
    #  first check that a nearly 0 slope will scan across the middle of the image.  Then try something at a tilt
    #m,c = 0.01, 1.0
    #m,c = 0.5, 0.5

    #  test value of binning width.  Set by user in end case (default 1.)
    w = 5.0
    #  test value of number of pixel-widths to include above and below trace.  Default 10 or 15?
    v = 10
    # Calculate vertical offset for bounds ahead and behind point along the trace
    offsetTrace = w * np.sqrt(m**2 + 1) / m
    # Calculate vertical offset for bounds above and below the trace
    offsetVertical = v * np.sqrt(m**2 + 1)
    offsetTrace, offsetVertical

    #  overlay trace on image, along with the
    xTrace = np.arange(1.0*xmin,xmax)
    yTrace = m*xTrace + c

    imgplot = plt.imshow(displayImg,zorder=0, extent = [xmin,xmax,ymin,ymax])
    ax2 = plt.subplot(plotSetting)
    ax2.plot(xTrace,yTrace, color='red')
    plt.show()

    #print(m,c,w,v,offsetTrace,offsetVertical)

    binWidth = w / np.sqrt(m**2+1)
    print(binWidth)

    #  make a test perpendicular and boundaries for point near X = 620

    p = 620.
    q = m * p + c
    ax3 = plt.subplot(plotSetting)
    ax3.plot(p,q, color='white', marker='*', markersize=20)
    plt.show()

    perp_m = -1 / m
    perp_c = q + p/m

    xPerp = 1.0*np.arange(p-20,p+20)
    yPerp = perp_m*xPerp + perp_c
    ax4 = plt.subplot(plotSetting)
    ax4.plot(xPerp,yPerp, color='red', linestyle='dashed')
    plt.show()

    yPerpHigh = yPerp + offsetTrace
    ax5 = plt.subplot(plotSetting)
    ax5.plot(xPerp,yPerpHigh, color='white', linestyle='dashed')
    plt.show()

    yPerpLow = yPerp - offsetTrace
    ax6 = plt.subplot(plotSetting)
    ax6.plot(xPerp,yPerpLow, color='white', linestyle='dashed')
    plt.show()

    yTraceHigh = yTrace + offsetVertical
    ax7 = plt.subplot(plotSetting)
    ax7.plot(xTrace,yTraceHigh, color='white', linestyle='dashed')
    plt.show()

    yTraceLow = yTrace - offsetVertical
    ax8 = plt.subplot(plotSetting)
    ax8.plot(xTrace,yTraceLow, color='white', linestyle='dashed')
    plt.show()

    #  show all nearby possible points
    subpoints = np.where((np.abs(xMap - p) < 20) & (np.abs(yMap - q) < 20))
    ax9 = plt.subplot(plotSetting)
    ax9.scatter(xMap[subpoints],yMap[subpoints], color='black', marker='.')
    plt.show()

    #  show all points within the box
    include = np.where((yMap < ((-1.0/m)*xMap + perp_c + offsetTrace)) & (yMap >= ((-1.0/m)*xMap + perp_c - offsetTrace)) & (yMap < (m*xMap + c + offsetVertical)) & (yMap >= (m*xMap + c - offsetVertical)))
    ax10 = plt.subplot(plotSetting)
    ax10.scatter(xMap[include],yMap[include], color='red', marker='o')
    plt.show()

    xUse = xMapi[include]
    yUse = yMapi[include]

    includedValues = img[yUse,xUse]

    fluxInBox = np.sum(includedValues) * xSample * ySample
    print(fluxInBox)

    testXsize = xLimHigh
    #  need to fix calculation of the number of needed bins.  Loop below iterates more times than can store
    i = 0
    for p in np.arange(0.0 + binWidth/2.0, testXsize+1, binWidth):
      i += 1

    pArray = np.zeros(i)
    qArray = np.zeros(i)
    spec1D = np.zeros(i)

    i = 0
    # scan across whole test image, in step size adjusting for slope
    # step in from lower limit by half the bin width
    for p in np.arange(0.0 + binWidth/2.0, testXsize+1, binWidth):
      # for p in np.arange(0.0 + binWidth/2.0, testXsize+1, 20*binWidth):
      #print(i)
      #pArray[i] = i
      #i += 1
      # Calculate the corresponding y coordinate to p (called q) on our long axis, from our regression, where y = mx + b.
      # (p, q) is a point along the center of our spectrum.
      q = m * p + c
      #print(m,c,p,q)
      #
      # Calculate slope and y-intercept for perpendicular line through point p,q
      perp_m = -1 / m
      perp_c = q + p/m
      #print(m,c,perp_m,perp_c,p,q)
      #
      # Store location of central point for each bin
      pArray[i] = p
      qArray[i] = q
      print(i,p,q)
      #
      #  test for points that fall within bounds
      #  get a 2 x n array of Y,X values for points in the subsampled image that fall within the bounds
      include = np.where((yMap < ((-1.0/m)*xMap + perp_c + offsetTrace)) & (yMap >= ((-1.0/m)*xMap + perp_c - offsetTrace)) & (yMap < (m*xMap + c + offsetVertical)) & (yMap >= (m*xMap + c - offsetVertical)))
      print(include)
      xUse = xMapi[include]
      print(xUse)
      yUse = yMapi[include]
      print(yUse)
      includedValues = img[yUse,xUse]
      print(includedValues)
      spec1D[i] = np.sum(includedValues) * xSample * ySample
      i += 1


      #  need to add some code to calculate distance along the trace

    plotSetting = 111
    ax11 = plt.subplot(plotSetting)
    ax11.plot(pArray,spec1D)
    plt.show()




      #  I don't know what I was thinking
      #  Now get the indices in the original image for those points (e.g., 1.3, 2.9 --> 1, 2)
      # 2 - y indices is a kludge to accommodate my coordinates, which are bottom left start
      # rather than Python's top left start
      # includedValues = img[[2-yMapi[include],xMapi[include]]]
      #
      #
      #  make an array to display to illustrate the selection of points from the original image
      #displayArray = np.zeros(xMap.shape)
      #displayArray[include] = includedValues
      #print(include, yMapi[include], xMapi[include], img[[2-yMapi[include],xMapi[include]]])
      #print(displayArray)
      #i += 1



    print(pArray, qArray, spec1D)
