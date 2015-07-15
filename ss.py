import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

pic = Image.open("127.tiff")
print(image)

x1, y2, x2, y2 = pic.getbbox()

a,b = [], []

for x in range(x1,x2):
    for y in range(y1,y2):
        pixel = pic.getpixel((x,y))
        if pixel[0]+pixel[1]+pixel[2] > 127:
            a.append(x)
            b.append(y2-y)
print(a)
print(b)
x, y = np.array(a), np.array(b)
# x = np.array([0,1,2,3])
# y = np.array([-1,0.2,0.9,2.1])

A = np.vstack([x, np.ones(len(x))]).T

print(A)

m,c = np.linalg.lstsq(A, y)[0]

print(m,c)
plt.plot(x,y,'o',label='original data', markersize = 10)
plt.plot(x, m*x + c, 'r', label = 'fitted line')
plt.legend()
plt.show()
