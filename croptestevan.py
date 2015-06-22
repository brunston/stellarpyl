import numpy as np



def cropnew(image, run=1):
 
    print('Run', run)
    duplicate = np.copy(image)
    counterPerRow = 0
    for i in range(len(duplicate[0])): 
        if np.array_equal(duplicate[0][i], np.array([0,0,0])):
            counterPerRow = counterPerRow + 1
        if counterPerRow == len(duplicate[0]):
            duplicate = np.delete(duplicate, 0, 0)
            print("Cropping row 0")
            print('Run', run, 'duplicate:')
            print(duplicate)
            cropnew(duplicate, run=run+1)
    print("duplicate right before return: \n", duplicate)
    return duplicate


def execute():
    img=np.array([[[0,0,0],[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0]]])
    img[2][1] = [1,1,1]
    img[3][2] = [2,2,2]
    print('Initial Image:')
    print(img)
    print('Shape:')
    print(img.shape)
    print("Running cropping script: \n")
    result = cropnew(img)
    return result

execute()