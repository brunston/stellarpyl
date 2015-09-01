def saanb(img, data, reg, threshold=127, r=1, twidth=10,spss=0.1):
    for x in our image:
        assign (0.5*r) as the points we want for the end-lines
        for x2 in our image:
            if x2 is within the end-line x value and within end-line y value:
                add pixel to dictionary
            if x2 is on end-line x value or on end-line y value:
                for subpixels in x2:
                    if they are within the end-line boundaries:
                    add to someCounter
                percentage to antialias = someCounter/(total possible)
                add to dictionary multiplying the pixel value by that percentage





Things to think about: how to deal with checking for y? what if\
the spectra is aligned like \ and not like /?
Then the y value comparison has to change (i.e. greater than and less than\
signs must be reversed)


------Current my saanb--------
def saanb():
    Grab prerequisites
    for x in image by step
        y = mx + c
        get upper and lower limits for the line compared to x

        for y2 in image by 1 #(i.e. moving down the image scanning horizontally)
            get a #value of (a,b) where (a,b) is along the line passing through x
                  #perpendicular to the trace

            determine the upper and lower limits for the line compared to a
            determine the upper and lower limits for the line compared to a (no rounding)

            for x2 in image:
                if x2 entirely within the limits
                    add the pixel to intensities
                
                if x2 is equal to either of the rounded limits:
                    determine which subpixels are inside the line

                get the percentage of subpixels
                multiply pixel by percentage, add to intensities



------current Scott saanb-----
Grab prerequisites
def parallel():
    return y intercept of line parallel to line with slope m, unit distance d away

get width
list of perpendiculars

for p in np.arange(x1,x2,0.1): #subpixel level (right?)
    get q using q = mp + c
    perp_m = -1/m
    perp_c = q
    perpendiculars.append((p,perp_c, parallel(-width), parellel(width)))

for all the pixels in our image
    for all the perpendiculars
    determine if x is between the end-lines

