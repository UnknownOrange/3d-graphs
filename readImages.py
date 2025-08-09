import imageio

def readImage(name):
    img = imageio.imread(name)
    print(img[55,55])
    return img


if __name__ == '__main__':
    incomeData = readImage("IncomeData.png")
    walkscoreData = readImage("WalkscoreData.png")