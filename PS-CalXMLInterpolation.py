import re
import math
import scipy.interpolate


def readXMLFile(filename):
    # Place contents of XML files into variable
    f = open(filename, 'r')
    x = f.readlines()
    f.close()
    return x

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


def insertCalFactor(index,newCFBlock):
    print(newCFBlock)
    print("IndexLoc {}".format(xmlDataNew[index]))


    print(newCFBlock)
    tempLength = len(newCFBlock)
    tempCounter = tempLength
    while tempCounter >= 1:
        tempCounter -= 1
        data = newCFBlock[tempCounter]

        xmlDataNew.insert(index, data)



def editCFblock(cfBlockList,frequency,calFactor,uncertainty):

    newCFBlock = cfBlockList.copy()

    for index, element in enumerate(newCFBlock):

        filterList1 = ['<OnLabel>', '<dB>', '<DUT_Power_Avg>', '<DeviationError>', '<RFOnStdDev>', '<DUT_Power_1>',
                       '<MisMatchFactor>']
        filterList2 = ['</OnLabel>', '</dB>', '</DUT_Power_Avg>', '</DeviationError>', '</RFOnStdDev>',
                       '</DUT_Power_1>', '</MisMatchFactor>']

        if ("<Frequency>" in element) and ("</Frequency>" in element):
            print(element)
            line = element.split(">")
            element1 = line[0] + ">"
            line = element.split("<")
            element2 = "<" + line[2]
            print(element1)
            print(element2)

            if frequency > 1:
                frequency = "{:,.0f}".format(frequency)
            else:
                frequency = "{:,.6f}".format(frequency)

            line = "{}{}{}".format(element1,frequency,element2)
            print(line)
            newCFBlock[index] = line

        elif ("<CalFactor>" in element) and ("</CalFactor>" in element):
            print(element)
            line = element.split(">")
            element1 = line[0] + ">"
            line = element.split("<")
            element2 = "<" + line[2]
            print(element1)
            print(element2)

            calFactor = "{:.4f}".format(calFactor)

            line = "{}{}{}".format(element1,calFactor,element2)
            print(line)
            newCFBlock[index] = line

        elif ("<Uncertainty>" in element) and ("</Uncertainty>" in element):
            print(element)
            line = element.split(">")
            element1 = line[0] + ">"
            line = element.split("<")
            element2 = "<" + line[2]
            print(element1)
            print(element2)

            uncertainty = "{:.4f}".format(uncertainty)

            line = "{}{}{}".format(element1,uncertainty,element2)
            print(line)
            newCFBlock[index] = line
        else:
            for index2, i in enumerate(filterList1):

                filter1 = i
                filter2 = filterList2[index2]

                if (filter1 in element) and (filter2 in element):
                    print(element)
                    line = element.split(">")
                    element1 = line[0] + ">"
                    line = element.split("<")
                    element2 = "<" + line[2]
                    print(element1)
                    print(element2)

                    insert = "- -"

                    line = "{}{}{}".format(element1, insert, element2)
                    # print(line)
                    # print("--------------------------------------------")
                    # print("filter1 {}".format(filter1))
                    # print("filter2 {}".format(filter2))
                    # print("element {}".format(element))
                    # print("line {}".format(line))
                    newCFBlock[index] = line
                    # print("newCFBlock {}".format(newCFBlock))
                    # input("Press Any Key To Continue...")



    return newCFBlock

# Start Program =================================================================
filename = "test2.XML"
xmlData = readXMLFile(filename)


rhoFreqList = []
cfFreqList = []
cfList = []
uncList = []

# Read in the existing Rho and CF data
for index, line in enumerate(xmlData):

    if ("RhoData diffgr" in line):
        lineList = line.split(" ")
        rFreq = xmlData[index + 1]
        rFreq = re.sub("[^0-9.]", "", rFreq)
        rFreq = float(rFreq)
        rhoFreqList.append(rFreq)

    if ("CalFactor diffgr" in line):
        lineList = line.split(" ")
        cFreq = xmlData[index + 1]
        cFreq = re.sub("[^0-9.]", "", cFreq)
        cFreq = float(cFreq)
        cfFreqList.append(cFreq)

        cf = xmlData[index + 2]
        cf = re.sub("[^0-9.]", "", cf)
        cf = float(cf)
        cfList.append(cf)

        unc = xmlData[index + 3]
        unc = re.sub("[^0-9.]", "", unc)
        unc = float(unc)
        uncList.append(unc)

cfFreqListNew = []
cfListNew = []
uncListNew = []
requiredInterpList = []
for index, freq in enumerate(rhoFreqList):

    if (freq in cfFreqList):
        cfFreqListNew.append(freq)

        tempIndex = cfFreqList.index(freq)
        tempValue = cfList[tempIndex]
        cfListNew.append(tempValue)

        tempValue = uncList[tempIndex]
        uncListNew.append(tempValue)

        requiredInterpList.append(0)
    else:
        cfFreqListNew.append(float(0))
        cfListNew.append(float(0))
        uncListNew.append(float(0))

        requiredInterpList.append(1)


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



# Create Cal Factor Points Template by copying existing CF block into list
tempBool = False
cfBlockList = []
for index, line in enumerate(xmlData):

    if tempBool == True:
        break

    if ("CalFactor diffgr" in line):
        cfBlockList.append(line)

        tempCounter = 1
        while tempBool == False:
            line2 = xmlData[index + tempCounter]
            cfBlockList.append(line2)
            tempCounter += 1
            if ("</CalFactor>" in line2) and (not "<CalFactor>" in line2):
                tempBool = True

cfBlockLength = len(cfBlockList)
# print(cfBlockList)

# print(cfFreqListNew)
# print(cfListNew)
# print(uncListNew)
# print(requiredInterpList)
#
# print(len(cfFreqListNew))
# print(len(cfListNew))
# print(len(uncListNew))
# print(len(requiredInterpList))

# print(cfBlockList)
# print(newCFblock)



# Determine where an interpolated CF block needs to be entered into the existing data
xmlDataNew = xmlData.copy()
for index, element in enumerate(requiredInterpList):

    if element == 1:
        freqToAdd = cfFreqListNew[index]
        CFToAdd = cfListNew[index]
        uncertaintyToAdd = uncListNew[index]

        print("freqToAdd {}".format(freqToAdd))

        for index2, line in enumerate(xmlData):

            if ("CalFactor diffgr" in line):
                # Get the current frequency of the CF block
                lineList = xmlData[index2 + 1]
                # print(lineList)
                freq = re.sub("[^0-9.]", "", lineList)
                freq = float(freq)
                #print("freq {}".format(freq))

                if freq > freqToAdd:

                    newCFBlock = editCFblock(cfBlockList, freqToAdd, CFToAdd, uncertaintyToAdd)
                    tempIndex = index2
                    print("newCFBlock {}".format(newCFBlock))
                    print("cfBlockLength {}".format(cfBlockLength))

                    print("tempIndex {}".format(tempIndex))

                    insertCalFactor(tempIndex,newCFBlock)
                    break


with open('test0001.xml', 'w') as filehandle:
    for listitem in xmlDataNew:
        filehandle.write(listitem)



