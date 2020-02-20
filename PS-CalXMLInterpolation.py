import re
import math
import scipy.interpolate


def readXMLFile(filename):
    # Place contents of XML files into variable
    f = open(filename, 'r')
    x = f.readlines()
    f.close()
    return x

# print(rhoFreqList)
# print(cfFreqListNew)
# print(cfListNew)
# print(uncListNew)

def interpStart(x,x1,x2,y1,y2):
    a1 = x2 - x1
    a2 = y2 - y1
    a3 = a2 / a1
    a4 = x1 - x

    y = y1 - (a4 * a3)
    return y

def interpEnd(x,x1,x2,y1,y2):
    a1 = x2 - x1
    a2 = y2 - y1
    a3 = a2 / a1
    a4 = x - x2

    y = y2 + (a4 * a3)
    return y

def interpMid(x,x1,x2,y,y2):
    a1 = x2 - x
    a2 = y2 - y
    a3 = a2 / a1
    a4 = x1 - x

    y1 = y + (a4 * a3)
    return y1

def interpolation(yVal,x,y):

    # print(x)
    # print(y)
    # print(yVal)
    y_interp = scipy.interpolate.interp1d(x, y)
    return(y_interp(yVal))

def performInterpolation():

    for index, freq in enumerate(rhoFreqList):

        cfFreqListNewFreq = cfFreqListNew[index]
        if cfFreqListNewFreq == 0:

            cfFreqListNew[index] = freq

            x = rhoFreqList.copy()

            newCFVal = float(interpolation(freq, xVals, yValsCF))
            newUncVal = interpolation(freq, xVals, yValsUNC)

            unc1 = newUncVal**2
            unc2 = newUncVal ** 2
            unc3 = unc1+unc2
            newUncVal = math.sqrt(unc3)

            cfListNew[index] = newCFVal
            uncListNew[index] = newUncVal

filename = "test2.XML"
x = readXMLFile(filename)


rhoFreqList = []
cfFreqList = []
cfList = []
uncList = []

# Read in the existing Rho and CF data
for index, line in enumerate(x):

    if ("RhoData diffgr" in line):
        lineList = line.split(" ")
        rFreq = x[index + 1]
        rFreq = re.sub("[^0-9.]", "", rFreq)
        rFreq = float(rFreq)
        rhoFreqList.append(rFreq)

    if ("CalFactor diffgr" in line):
        lineList = line.split(" ")
        cFreq = x[index + 1]
        cFreq = re.sub("[^0-9.]", "", cFreq)
        cFreq = float(cFreq)
        cfFreqList.append(cFreq)

        cf = x[index + 2]
        cf = re.sub("[^0-9.]", "", cf)
        cf = float(cf)
        cfList.append(cf)

        unc = x[index + 3]
        unc = re.sub("[^0-9.]", "", unc)
        unc = float(unc)
        uncList.append(unc)

cfFreqListNew = []
cfListNew = []
uncListNew = []
for index, freq in enumerate(rhoFreqList):

    if (freq in cfFreqList):
        cfFreqListNew.append(freq)

        tempIndex = cfFreqList.index(freq)
        tempValue = cfList[tempIndex]
        cfListNew.append(tempValue)

        tempValue = uncList[tempIndex]
        uncListNew.append(tempValue)
    else:
        cfFreqListNew.append(float(0))
        cfListNew.append(float(0))
        uncListNew.append(float(0))


# print(cfFreqListNew)
# print(cfListNew)
# print(uncListNew)

xVals = []
yValsCF = []
yValsUNC = []
for index, freq in enumerate(rhoFreqList):

    if (freq in cfFreqList):
        xVals.append(freq)

        tempIndex = cfFreqListNew.index(freq)
        tempValue = cfListNew[tempIndex]
        yValsCF.append(tempValue)

        tempValue = uncListNew[tempIndex]
        yValsUNC.append(tempValue)


# print(xVals)
# print(yValsCF)
# print(yValsUNC)
#
# print(len(xVals))
# print(len(yValsCF))
# print(len(yValsUNC))


performInterpolation()

print(cfFreqListNew)
print(cfListNew)
print(uncListNew)

print(len(cfFreqListNew))
print(len(cfListNew))
print(len(uncListNew))







