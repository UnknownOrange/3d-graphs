from statistics import stdev

import imageio
import statistics
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from matplotlib.ticker import LinearLocator

width = 928
height = 1022

avgSample = 3

def getSurroundingAverage(img,xPos,yPos):

    data = []

    for a in range (-1*avgSample,avgSample,1):
        for b in range(-1*avgSample,avgSample,1):

            if xPos+a>0 and xPos+a < width and yPos+b>0 and yPos+b < height:
                if img[xPos+a,yPos+b][0] > 10:
                    data.append(img[xPos+a,yPos+b][0]+1)


    if len(data) == 0:
        return 0

    total = 0.0

    st_dev = np.std(data)

    for item in data:
        total = total + item

    avg = total/len(data)


    #Ignore outliers
    total2 = 0.0
    values = 0.0
    for item in data:

        if (avg-item)<st_dev*2:
            values = values + 1
            total2+= item

    if values == 0:
        return 100

    result = total2/values
    if result<100:
        return 100
    return result

def smooth(data,x,y, size):

    tmp = []

    for a in range (-1*size,size,1):
        for b in range(-1*size,size,1):
            if 0 < x+a < width and 0 < y+b < height:
                tmp.append(data[x+a,y+b])

    total = 0
    st_dev = 0


    st_dev = np.std(tmp)

    for item in tmp:
        if item > 20:
            total = total + item


    if len(tmp) == 0:
        return 0

    avg1 = total /len(tmp)
    return avg1

    total2 = 0.0
    ct = 0
    for item in tmp:

        if  (avg1-item)<st_dev:
            ct+=1
            total2 = total2 + item

    if ct == 0:
        return data[x,y]
    return total2/ct

def readImageAndSmooth(name):
    img = imageio.imread(name)



    data = []

    for x in range(0, width):
        print(x)
        row = []
        for y in range(0, height):
            color = getSurroundingAverage(img,x,y)
            row.append(color)

        data.append(row)


    return np.array(data)

def readImage(name):
    img = imageio.imread(name)



    data = []

    for x in range(0, width):
        print(x)
        row = []
        for y in range(0, height):

            if img[x,y][0]<150:
                row.append(150)
            else:
                row.append(img[x,y][0])

        data.append(row)


    return np.array(data)


if __name__ == '__main__':
    incomeData = readImage("IncomeData.png")
    walkscoreData = readImageAndSmooth("WalkscoreData.png")

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    print ("Item:"+str(incomeData[50,50]))

    for a in range(0,15):
        print(a)
        for x in range(0, width):
            for y in range(0, height):
                walkscoreData[x,y]=smooth(walkscoreData,x,y,1)

    # Make data.
    X = np.arange(0, 1022, 1)
    Y = np.arange(0, 928, 1)
    X, Y = np.meshgrid(X, Y)
    R = incomeData
    Z = walkscoreData

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_zlim(-1.01, 250.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.02f}')

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.gca().invert_xaxis()
    plt.show()

# my-venv/bin/python3 readImages.py