import re
import math
import scipy.interpolate

from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time


def yesNoGUI(questionStr, windowName=""):
    root = Tk()

    canvas1 = tk.Canvas(root, width=1, height=1)
    canvas1.pack()

    MsgBox = tk.messagebox.askquestion(windowName, questionStr, icon='warning')
    if MsgBox == 'yes':
        # root.destroy()
        # print(1)
        response = True
    else:
        # tk.messagebox.showinfo('Return', 'You will now return to the application screen')
        response = False

    # ExitApplication()
    root.destroy()
    return response


def getFilePath(extensionType, initialDir="", extensionDescription="", multi=False):
    root = Tk()

    canvas1 = tk.Canvas(root, width=1, height=1)
    canvas1.pack()

    if multi == True:
        root.filenames = filedialog.askopenfilenames(initialdir=initialDir, title="Select file",
                                                     filetypes=(
                                                     (extensionDescription, extensionType), ("all files", "*.*")))
        list = root.filenames
    else:
        root.filename = filedialog.askopenfilename(initialdir=initialDir, title="Select file",
                                                   filetypes=(
                                                   (extensionDescription, extensionType), ("all files", "*.*")))
        list = root.filename
    root.destroy()
    return list


def getDirectoryPath(initialDir=""):
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(initialdir=initialDir)
    root.destroy()
    return folder_selected


def popupMsg(msg, popTitle=""):
    popup = tk.Tk()
    popup.wm_title(popTitle)
    label = ttk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def getTextEntry(buttonText="", labelText="", titleText=""):
    root = Tk()
    root.title(titleText)

    mystring = StringVar()

    def getvalue():
        global output

        output = mystring.get()

        root.destroy()

    Label(root, text=labelText).grid(row=0, sticky=W)  # label
    Entry(root, textvariable=mystring).grid(row=0, column=1, sticky=E)  # entry textbox

    WSignUp = Button(root, text=buttonText, command=getvalue).grid(row=3, column=0, sticky=W)  # button

    root.mainloop()
    return output


def yesNoPrompt(message, titleText=""):
    root = tk.Tk()  # create window

    canvas1 = tk.Canvas(root, width=0, height=0)
    canvas1.pack()

    MsgBox = tk.messagebox.askquestion(titleText, message,
                                       icon='warning')
    if MsgBox == 'yes':
        response = True
        root.destroy()
    else:
        response = False
        root.destroy()

    root.mainloop()
    return response


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
            newDbVal = float(interpolation(freq, xVals, yValsDb))

            # Take the interpolated uncertainty value and RSS double it
            unc1 = newUncVal ** 2
            unc2 = newUncVal ** 2
            unc3 = unc1+unc2
            newUncVal = math.sqrt(unc3)

            cfListNew[index] = newCFVal
            uncListNew[index] = newUncVal
            dbListNew[index] = newDbVal


def insertCalFactor(index,newCFBlock):
    # print(newCFBlock)
    # print("IndexLoc {}".format(xmlDataNew[index]))
    #
    #
    # print(newCFBlock)
    tempLength = len(newCFBlock)
    tempCounter = tempLength
    while tempCounter >= 1:
        tempCounter -= 1
        data = newCFBlock[tempCounter]

        xmlDataNew.insert(index, data)





def editCFblock(cfBlockList,frequency,calFactor,uncertainty,dB):

    newCFBlock = cfBlockList.copy()

    for index, element in enumerate(newCFBlock):

        filterList1 = ['<OnLabel>', '<DUT_Power_Avg>', '<DeviationError>', '<RFOnStdDev>', '<DUT_Power_1>',
                       '<MisMatchFactor>']
        filterList2 = ['</OnLabel>', '</DUT_Power_Avg>', '</DeviationError>', '</RFOnStdDev>',
                       '</DUT_Power_1>', '</MisMatchFactor>']

        if ("<Frequency>" in element) and ("</Frequency>" in element):
            # print(element)
            line = element.split(">")
            element1 = line[0] + ">"
            line = element.split("<")
            element2 = "<" + line[2]
            # print(element1)
            # print(element2)

            if frequency > 1:
                frequency = "{:,.0f}".format(frequency)
            else:
                frequency = "{:,.6f}".format(frequency)

            line = "{}{}{}".format(element1,frequency,element2)
            # print(line)
            newCFBlock[index] = line

        elif ("<CalFactor>" in element) and ("</CalFactor>" in element):
            # print(element)
            line = element.split(">")
            element1 = line[0] + ">"
            line = element.split("<")
            element2 = "<" + line[2]
            # print(element1)
            # print(element2)

            calFactor = "{:.4f}".format(calFactor)

            line = "{}{}{}".format(element1,calFactor,element2)
            # print(line)
            newCFBlock[index] = line

        elif ("<Uncertainty>" in element) and ("</Uncertainty>" in element):
            # print(element)
            line = element.split(">")
            element1 = line[0] + ">"
            line = element.split("<")
            element2 = "<" + line[2]
            # print(element1)
            # print(element2)

            uncertainty = "{:.4f}".format(uncertainty)

            line = "{}{}{}".format(element1,uncertainty,element2)
            # print(line)
            newCFBlock[index] = line

        elif ("<dB>" in element) and ("</dB>" in element):
            # print(element)
            line = element.split(">")
            element1 = line[0] + ">"
            line = element.split("<")
            element2 = "<" + line[2]
            # print(element1)
            # print(element2)

            # print("dB: {}".format(dB))
            dB = "{:.4f}".format(dB)
            # print("dB: {}".format(dB))

            line = "{}{}{}".format(element1,dB,element2)
            # print(line)
            newCFBlock[index] = line

        else:
            for index2, i in enumerate(filterList1):

                filter1 = i
                filter2 = filterList2[index2]

                if (filter1 in element) and (filter2 in element):
                    # print(element)
                    line = element.split(">")
                    element1 = line[0] + ">"
                    line = element.split("<")
                    element2 = "<" + line[2]
                    # print(element1)
                    # print(element2)

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
dbList = []

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
        print("cfFreq: {}".format(cFreq))
        cFreq = re.sub("[^0-9.]", "", cFreq)
        print("cfFreq: {}".format(cFreq))
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

        db = xmlData[index + 5]
        db = re.sub("[^0-9.-]", "", db)
        db = float(db)
        dbList.append(db)

print(rhoFreqList)
print(dbList)
# Create new lists for each fields requiring interp which are equal length to the rhoFreq list
cfFreqListNew = []
cfListNew = []
uncListNew = []
dbListNew = []
requiredInterpList = []
for index, freq in enumerate(rhoFreqList):

    # If the point does not require interp then insert the already existing value
    if (freq in cfFreqList):
        cfFreqListNew.append(freq)

        tempIndex = cfFreqList.index(freq)
        tempValue = cfList[tempIndex]
        cfListNew.append(tempValue)

        tempValue = uncList[tempIndex]
        uncListNew.append(tempValue)

        tempValue = dbList[tempIndex]
        dbListNew.append(tempValue)

        # Tracks which points require interp (1 means required, 0 means not required)
        requiredInterpList.append(0)

    # If the point requires interp then fill it with 0 for now
    else:
        cfFreqListNew.append(float(0))
        cfListNew.append(float(0))
        uncListNew.append(float(0))
        dbListNew.append(float(0))

        # Tracks which points require interp (1 means required, 0 means not required)
        requiredInterpList.append(1)


# print(cfFreqListNew)
# print(cfListNew)
# print(uncListNew)

xVals = []
yValsCF = []
yValsUNC = []
yValsDb = []
for index, freq in enumerate(rhoFreqList):

    if (freq in cfFreqList):
        xVals.append(freq)

        tempIndex = cfFreqListNew.index(freq)
        tempValue = cfListNew[tempIndex]
        yValsCF.append(tempValue)

        tempValue = uncListNew[tempIndex]
        yValsUNC.append(tempValue)

        tempValue = dbListNew[tempIndex]
        yValsDb.append(tempValue)


# Perform interpolation process for all missing points
performInterpolation()

# Create Cal Factor Points XML Template by copying existing CF XML block into list
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
        dbToAdd = dbListNew[index]

        # print("freqToAdd {}".format(freqToAdd))

        for index2, line in enumerate(xmlData):

            if ("CalFactor diffgr" in line):
                # Get the current frequency of the CF block
                lineList = xmlData[index2 + 1]
                # print(lineList)
                freq = re.sub("[^0-9.]", "", lineList)
                freq = float(freq)
                #print("freq {}".format(freq))

                if freq > freqToAdd:

                    newCFBlock = editCFblock(cfBlockList, freqToAdd, CFToAdd, uncertaintyToAdd,dbToAdd)
                    tempIndex = index2
                    # print("newCFBlock {}".format(newCFBlock))
                    # print("cfBlockLength {}".format(cfBlockLength))
                    #
                    # print("tempIndex {}".format(tempIndex))

                    insertCalFactor(tempIndex,newCFBlock)
                    break

    # The original xmlData needs to be updated each time new data is added
    xmlData = xmlDataNew.copy()

# Go through the XML data in the variable and update the row order of the CF data
tempBool = False
cfBlockList = []
rowOrderCounter = 0
calFactorCounter = 1
hiddenIndexCounter = 0
for index, line in enumerate(xmlDataNew):

    if tempBool == True:
        break

    if ("CalFactor diffgr" in line):

        # Split out the line so it can be searched and updated easily
        splitLine = line.split("\"")
        # print(splitLine)

        # Find the list element for the row number
        for index2, element in enumerate(splitLine):
            loweredElemet = element.lower()
            if ("roworder" in loweredElemet):
                splitLine[index2+1] = str(rowOrderCounter)

        # Iterate the newly updated splitLine list back into a string
        newLine = ""
        for index2, element in enumerate(splitLine):
            newLine+=str(element) + "\""
        # Delete the final " from the end of the string
        newLine = newLine[:-1:]

        # Update the existing CSV variable data with the updated newLine
        xmlDataNew[index] = newLine

        rowOrderCounter += 1
        calFactorCounter += 1
        hiddenIndexCounter += 1






            # if ("</CalFactor>" in line2) and (not "<CalFactor>" in line2):
            #     tempBool = True



# Write the XML data to a file
with open('test0001.xml', 'w') as filehandle:
    for listItem in xmlDataNew:
        # print(listItem)
        filehandle.write(listItem)



