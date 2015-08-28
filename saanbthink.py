def saanb(img, data, reg, threshold=127, r=1, twidth=10,spss=0.1):
	for x in our image:
		assign (0.5*r) as the points we want for the end-lines
		get the lines which run perpendicular to the trace at those x values
		for subpixels in x:
			if they are within the end-line boundaries:
				add to someCounter
		percentage to antialias = someCounter/(total possible)
		add to dictionary multiplying the pixel value by that percentage

Things to think about: how to deal with checking for y? what if\
the spectra is aligned like \ and not like /?
Then the y value comparison has to change (i.e. greater than and less than\
signs must be reversed)
