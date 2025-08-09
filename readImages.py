import imageio

import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from matplotlib.ticker import LinearLocator

width = 928
height = 1022

def getSurroundingAverage(img,x,y):

    data = []
    if x>10 and x <width-10 and y>10 and y<height-10:

        for a in range (-10,10):
            for b in range(-10,10):
                if img[x+a,y+b] !=0:
                    data.append(img[x+a,y+b][0])


    if len(data) == 0:
        return 0

    total = 0.0
    for item in data:
        total = total + item
    print(total)
    return total/len(data)

def readImage(name):
    img = imageio.imread(name)



    data = []

    for x in range(0, width):
        row = []
        for y in range(0, height):

            color = img[x,y][0]

            if img[x,y][1] == 0:
                color = getSurroundingAverage(img,x,y)

            row.append(color)
        data.append(row)


    return np.array(data)


if __name__ == '__main__':
    incomeData = readImage("IncomeData.png")
    walkscoreData = readImage("WalkscoreData.png")

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    print ("Item:"+str(incomeData[50,50]))


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

    plt.show()