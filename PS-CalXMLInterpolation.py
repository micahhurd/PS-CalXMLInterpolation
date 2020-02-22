# PS-Cal XML Cal Factor Interpolator
# By Micah Hurd
programName = "PS-Cal XML Cal Factor Interpolator"
version = 1.1

import re
import math
import scipy.interpolate
import os
import shutil
import os.path
from os import path
from pathlib import Path
from distutils.dir_util import copy_tree

from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time

def readConfigFile(filename, searchTag, sFunc=""):
    searchTag = searchTag.lower()
    # print("Search Tag: ",searchTag)

    # Open the file
    with open(filename, "r") as filestream:
        # Loop through each line in the file

        for line in filestream:

            if line[0] != "#":

                currentLine = line
                equalIndex = currentLine.find('=')
                if equalIndex != -1:

                    tempLength = len(currentLine)
                    # print("{} {}".format(equalIndex,tempLength))
                    tempIndex = equalIndex
                    configTag = currentLine[0:(equalIndex)]
                    configTag = configTag.lower()
                    configTag = configTag.strip()
                    # print(configTag)

                    configField = currentLine[(equalIndex + 1):]
                    configField = configField.strip()
                    # print(configField)

                    # print("{} {}".format(configTag,searchTag))
                    if configTag == searchTag:

                        # Split each line into separated elements based upon comma delimiter
                        # configField = configField.split(",")

                        # Remove the newline symbol from the list, if present
                        lineLength = len(configField)
                        lastElement = lineLength - 1
                        if configField[lastElement] == "\n":
                            configField.remove("\n")
                        # Remove the final comma in the list, if present
                        lineLength = len(configField)
                        lastElement = lineLength - 1

                        if configField[lastElement] == ",":
                            configField = configField[0:lastElement]

                        lineLength = len(configField)
                        lastElement = lineLength - 1

                        # Apply string manipulation functions, if requested (optional argument)
                        if sFunc != "":
                            sFunc = sFunc.lower()

                            if sFunc == "listout":
                                configField = configField.split(",")

                            if sFunc == "stringout":
                                configField = configField.strip("\"")

                            if sFunc == "int":
                                configField = int(configField)

                            if sFunc == "float":
                                configField = float(configField)

                        filestream.close()
                        return configField

        filestream.close()
        return "Searched term could not be found"

def create_log(log_file):
    f = open(log_file, "w+")

    f.close()
    return 0

def userInterfaceHeader(program, version, cwd, logFile, msg=""):
    print(program + ", Version " + str(version))
    print("Current Working Directory: " + str(cwd))
    print("Log file located at working directory: " + str(logFile))
    print("=======================================================================")
    if msg != "":
        print(msg)
        print("_______________________________________________________________________")
    return 0

def clear():  # Clears the console
    # for windows
    from os import system, name
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

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
# Set initial program variables --------------------
logFile = "interplog.txt"
if os.path.isfile(logFile):
    # print ("Log File Exists")
    logFile = logFile
else:
    create_log(logFile)

cwd = os.getcwd() + "\\"
clear()
userInterfaceHeader(programName, version, cwd, logFile)
print("__________  _________         _________         __ ")
print("\______   \/   _____/         \_   ___ \_____  |  |")
print(" |     ___/\_____  \   ______ /    \  \/\__  \ |  |")
print(" |    |    /        \ /_____/ \     \____/ __ \|  |__")
print(" |____|   /_______  /          \______  (____  /____/")
print("                  \/                  \/     \/      ")
print(" ___        __                              __          __        ")
print("|   | _____/  |_  _________________   ____ |  | _____ _/  |_  ___________ ")
print("|   |/    \   __\/ __ \_  __ \____ \ /  _ \|  | \__  \\   __\/  _ \_  __ \\")
print("|   |   |  \  | \  ___/|  | \/  |_> >  <_> )  |__/ __ \|  | (  <_> )  | \/")
print("|___|___|  /__|  \___  >__|  |   __/ \____/|____(____  /__|  \____/|__|")
print("         \/          \/      |__|                    \/                   ")
print("=======================================================================")


# Pull in settings from the config file ------------
configFile = "interpolator.cfg"

debug = readConfigFile(configFile, "debug", "int")
PS_CalResultsFolder = readConfigFile(configFile, "PS_CalResultsFolder")
archivePath = readConfigFile(configFile, "archivePath")
standardsDataFolder = readConfigFile(configFile, "standardsDataFolder")
interpReferenceMethod = readConfigFile(configFile, "interpReferenceMethod", "int")

# Set debug flag
if debug == 1:
    debugBool = True
else:
    debugBool = False

# Load XML file for interpolation ---------------------------------------------
if debugBool == True:
    xmlFile = "test3.XML"
    xmlFilePath = cwd + xmlFile
else:
    print("Use the file dialogue window to select the XML file for interpolation...")
    extensionType = "*.XML"
    xmlFilePath = getFilePath(extensionType,initialDir=PS_CalResultsFolder,extensionDescription="PSCAL XML")

    # Split out the xmlFilePath to obtain the xmlFile name itself
    tempList = xmlFilePath.split("/")
    xmlFile = tempList[-1]

# Read-in the XML file calibration data to a list
xmlData = readXMLFile(xmlFilePath)

# Setup to allow for interpolation to occur via the alternate reference method (using the Standard's data as the ref)
# The alternate method was introduced later, so the code below only massages the xmlFile data into a state where
# it can be interpolated by the normal method. Thereafter the normal method is used.
if interpReferenceMethod == 2:
    if debugBool == True:
        standardDataFile = "3538.XML"
        xmlFilePath = cwd + xmlFile
    else:
        print("Use the file dialogue window to select the XML data file of the standard used for the sensor cal...")
        extensionType = "*.XML"
        standardDataFile = getFilePath(extensionType, initialDir=PS_CalResultsFolder, extensionDescription="PSCAL XML")

    stdXMLData = readXMLFile(standardDataFile)

    # Pull the frequency of all available cal points from the standard data
    stdFreqList = []
    for index, line in enumerate(stdXMLData):

        if ("Data diffgr:id" in line):
            rFreq = stdXMLData[index + 1]
            rFreq = re.sub("[^0-9.]", "", rFreq)
            rFreq = float(rFreq)
            stdFreqList.append(rFreq)

    # print(stdFreqList)
    # input("Press Enter To Continue...")

    # Build a list of CF frequencies present in the XML calibration data
    cfFreqList = []
    for index, line in enumerate(xmlData):

        if ("CalFactor diffgr" in line):
            lineList = line.split(" ")
            cFreq = xmlData[index + 1]
            cFreq = re.sub("[^0-9.]", "", cFreq)
            cFreq = float(cFreq)
            cfFreqList.append(cFreq)

    # Compare the cfFreqList to the freqs contained in the standard's data to list which require interpolation
    requiredInterpList = []
    for index, i in enumerate(cfFreqList):

        # Check if the cf Freq is in the standard data list; if not then set required interp to 1
        try:
            tempIndex = stdFreqList.index(i)
            requiredInterpList.append(0)
        except:
            requiredInterpList.append(1)

    # Delete CF blocks from existing XML data for all frequencies that must be interpolated
    # Missing CF blocks is what triggers the normal method to know that interpolation must occur
    for index, i in enumerate(requiredInterpList):
        if i == 1:
            tempFreq = cfFreqList[index]

            for index2, line in enumerate(xmlData):
                if ("CalFactor diffgr" in line):
                    checkFreq = xmlData[index2 + 1]
                    checkFreq = re.sub("[^0-9.]", "", checkFreq)
                    checkFreq = float(checkFreq)
                    if checkFreq == tempFreq:
                        del xmlData[index2]
                        tempBool = False
                        while tempBool == False:
                            if ("CalFactor diffgr" in xmlData[index2]):
                                tempBool = True
                            else:
                                del xmlData[index2]


# Create backup copy of existing XML file
tempBool = path.exists(archivePath)
if tempBool == True:
    tempBool = tempBool
else:
    os.mkdir(archivePath)


# Check if the file has already been backed up; if yes then create a unique name that will not overwrite the existing
archiveFilePath = archivePath + xmlFile
tempBool = path.exists(archiveFilePath)
tempCounter = 1
while tempBool == True:

    archiveFilePath = archivePath + xmlFile

    filename = Path(archiveFilePath)
    filename_wo_ext = filename.with_suffix('')
    archiveFilePath = str(filename_wo_ext)
    archiveFilePath+=" - Copy(" + str(tempCounter) +")"

    filename = Path(archiveFilePath)
    filename_replace_ext = filename.with_suffix('.xml')
    archiveFilePath = filename_replace_ext

    tempBool = path.exists(archiveFilePath)
    tempCounter+=1

# Backup of the original file
dest = shutil.copyfile(xmlFilePath, archiveFilePath)

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
        cFreq = re.sub("[^0-9.]", "", cFreq)
        cFreq = float(cFreq)
        cfFreqList.append(cFreq)

        cf = xmlData[index + 2]
        cf = re.sub("[^0-9.]", "", cf)
        # print("cf: {}".format(cf))
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
with open(xmlFilePath, 'w') as filehandle:
    for listItem in xmlDataNew:
        # print(listItem)
        filehandle.write(listItem)


print("")
print("* * INTERPOLATION COMPLETED * *")
print("")
print("Output file saved at: {}".format(xmlFilePath))
print("")
print("- - Open the XML file in PS-Cal to verify and save as PDF - -")
print("")
print("This program will close automatically in 5 seconds...")
time.sleep(5)
sys.exit()