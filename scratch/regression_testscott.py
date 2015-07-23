import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import math

image = Image.open("127.tiff")

x1, y1, x2, y2 = image.getbbox()

# Find our long axis by putting a line through all the points.
print(image.getbbox())
a = []
b = []

for x in range(x1, x2):
    for y in range(y1, y2):
        pixel = image.getpixel((x, y))
        if pixel[0] + pixel[1] + pixel[2] > 127:
            a.append(x)
            b.append(y)

x = np.array(a)
y = np.array(b)

A = np.vstack([x, np.ones(len(x))]).T

#print(A)

m, c = np.linalg.lstsq(A, y)[0]

print("m: {}  c: {}".format(m, c))

if 0:
    plt.plot(x, y, 'o', label='Original data', markersize=10)
    plt.plot(x, m * x + c, 'r', label='Fitted line')
    plt.legend()
    plt.show()

# Lamely re-use and b...
a,b = [], []

# Build a dictionary where the key is the x value on the long axis and the y value is the intensity.
intensities = {}

# n is our slope perpendicular
n = -1 / m

# Look all x values (called p) in our long axis.
for p in range(x1, x2):
    q = m * p + c

    # Now (p,q) is a point on our long axis.
    # Look at all points along our perpendicular to (p, q) in our image.
    for nx in np.arange(x1, x2 - 1, 0.1): # Hmm, -1 kludgy.
        ny = n * (nx - p) + q
        
        # now (nx, ny) is our point on our perpendicular
        if ny > y1 and ny < y2:
            # Look at all the pixels around (nx, ny) in a simple way, calculating how much of this pixel in the image we should grab.
            for nx_rounded in (math.floor(nx), math.ceil(nx)):
                for ny_rounded in (math.floor(ny), math.ceil(ny)):
                    if ny_rounded > y1 and ny_rounded < y2:
                        percent_nx = 1 - abs(nx - nx_rounded)
                        percent_ny = 1 - abs(ny - ny_rounded)
                        percent = percent_nx * percent_ny

                        # Sample the pixel and get an intensity.
                        pixel = image.getpixel((nx_rounded, ny_rounded))
                        value = percent * (pixel[0] + pixel[1] + pixel[2])

                        # If we have a value for this x value (knows as p) on our long axis, then add it to what we've got.
                        if p in intensities:
                            intensities[p] = intensities[p] + value
                        else:
                            intensities[p] = value

# Graph our intensity plot.
for graphx in intensities.keys():
    a.append(graphx)
    b.append(intensities[graphx])


x, y = np.array(a), np.array(b)

plt.plot(x, y, 'o', label='original data', markersize = 10)
plt.show()

