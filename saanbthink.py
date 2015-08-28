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