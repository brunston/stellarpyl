

# Approach 2

# Return y-intercept of line parallel to line with slope m, unit distance d away from it.
def parallel(m, b, d):
    return b - (d / math.sqrt(1 / m * m + 1)) * (m - 1 / m)

WIDTH = 3
perpendiculars = []    

# Build list of perpinducaltor tuples (x, .
# Look all x values (called p) in our long axis.
for p in np.arange(x1, x2, 0.1):
    # Calculate the corresponding y coordinate to p (called q) on our long axis, from our regression, where y = mx + b.
    # (p, q) is a point on our long axis.
    q = m * p + c

    # Slope of perpendicular is -1 / m, it's Y intercept is the value of the function at p.
    perp_m = -1 / m
    perp_c = q
    perpendiculars.append((p, perp_c, parallel(perp_m, perp_c, -WIDTH), parallel(perp_m, perp_c, WIDTH)))

# IGNORE
# if 0:
#     r = 0 
#     x = np.arange(-12, 12, 0.1)
#     for perp in perpendiculars:   
#         print("{} {} {} {}".format(r, perp[0], perp[1], perp[2]))
#         plt.plot(x, n * x + perp[1], 'r', label='Fitted liner m' + str(r))
#         plt.plot(x, n * x + perp[2], 'g', label='Fitted liner l' + str(r))
#         plt.plot(x, n * x + perp[3], 'b', label='Fitted liner r' + str(r))
#         r = r + 1
    
#     plt.legend()
#     plt.show()        

# public bool isLeft(Point a, Point b, Point c){
#    return ((b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)) > 0;
#}

def inverseF(m, y, b):
    return (y - b) / m
    
SAMPLING_FACTOR = 0.50

# For all the pixels in our image... 
for x in np.arange(x1, x2, SAMPLING_FACTOR):
    for y in np.arange(y1, y2, SAMPLING_FACTOR):
        # For all the perpendiculars to our long axis.
        for perp in perpendiculars:   
            # Determine if x is between the lines around the perpendicular.
            if x > inverseF(n, y, perp[2]) and x < inverseF(n, y, perp[3]):
                pixel = image.getpixel((math.floor(x), math.floor(y)))
                intensity = (pixel[0] + pixel[1] + pixel[2]) * SAMPLING_FACTOR
                p = perp[0]

                # If we have a value for this x value (known as p) on our long axis, then add it to what we've got.
                # Remember that the same p value will be picked for multiple intensities since we are using fractional nx's.
                if p in intensities:
                    intensities[p] = intensities[p] + intensity
                else:
                    intensities[p] = intensity

# Graph our intensity plot.
for graphx in intensities.keys():
    a.append(graphx)
    b.append(intensities[graphx])


x, y = np.array(a), np.array(b)
plt.plot(x, y, 'o', label='Original data', markersize=10)
plt.show()        
