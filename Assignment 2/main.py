# Andrew Sylvester and Cameron Meyer
# CS 4365 - Assignment 2 part 2
# main.py

import sys
import os.path
import re

#Global vars
domains = {}
constraints = []
chosenVars = []
varFile = None
conFile = None

#Functions
def assignDomain():
    global varFile
    global domains
    #Check if the var file is open
    if not varFile == None:
        #Read in each line of data to an array and remove unnecessary characters
        nextLine = varFile.readline()
        while(not nextLine == ""):
            line = re.split("[ :\n]", nextLine)
            emptyCount = line.count('')
            for i in range(emptyCount):
                line.remove('')
            variable = line[0]
            line.remove(line[0])

            #Convert domains to integers and update the domains dictionary
            numbers = []
            for num in line:
                numbers.append(int(num))
            domains.update({variable : numbers})
            nextLine = varFile.readline()

def assignConstraints():
    global conFile
    global constraints
    #Check if the con file is open
    if not conFile == None:
        #Read in each line of data to an array and remove unnecessary characters
        nextLine = conFile.readline()
        while(not nextLine == ""):
            line = re.split("[ :\n]", nextLine)
            emptyCount = line.count('')
            for i in range(emptyCount):
                line.remove('')

            #Convert each constraint to a tuple and update the array of constraints
            constraints.append(tuple(line))
            nextLine = conFile.readline()

def backtrack():
    print(mostConstrained())

def forwardCheck():
    print("ForwardChecking")

def mostConstrained():
    mostConList = []
    smallestDomain = 99
    #Find smallest domains
    for var in domains:
        if len(domains[var]) < smallestDomain:
            mostConList = [var]
            smallestDomain = len(domains[var])
        elif len(domains[var]) == smallestDomain:
            mostConList.append(var)
    #Check if only one value, otherwise use most constraining
    if len(mostConList) == 1:
        return mostConList[0]
    else:
        return mostConstraining(mostConList)

def mostConstraining(valList):
    mostConst = 0
    mostConstVar = ""
    for val in valList:
        numOfConstraints = 0
        for constraint in constraints:
            if (val == constraint[0] or val == constraint[2]) and (constraint[0] not in chosenVars and constraint[2] not in chosenVars):
                numOfConstraints += 1
        if numOfConstraints > mostConst:
            mostConstVar = val
            mostConst = numOfConstraints
    #This will be alphabetical even on a tie since the input will always be provided alphabetical.
    return mostConstVar

#Not Needed
def alphabetical(valLists):
    return "Var"

#Attempt to open files, return true if successful
def openFiles():
    #Check if the given .var file exists
    if(os.path.isfile(sys.argv[1])):
        global varFile
        varFile = open(sys.argv[1], "r")
    else:
        print('.var file does not exist.')
        return False

    #Check if the given .con file exists
    if(os.path.isfile(sys.argv[2])):
        global conFile
        conFile = open(sys.argv[2], "r")
    else:
        print('.con file does not exist.')
        return False
    #The files were successfully opened
    return True

def closeFiles():
    #Close files as needed
    if(not varFile == None):
        varFile.close()
    if(not conFile == None):
        conFile.close()

#Include logic for reading command line, files, and main processes here.
#Check for exact number of command line arguments
if not len(sys.argv) == 4:
    print('Invalid number of arguments. Searching for 3 arguments and found ', len(sys.argv) - 1, '.') #Looking for 3 args besides the python filename
    exit()

#Check if we were given the name of a .var file first
if not sys.argv[1].find(".var") == len(sys.argv[1]) - 4:
    print('.var file not found in argument 1.')
    exit()

#Check if we were given the name of a .con file second
if not sys.argv[2].find(".con") == len(sys.argv[2]) - 4:
    print('.con file not found in argument 2.')
    exit()

if openFiles():
    assignDomain()
    assignConstraints()
else:
    exit()

#Check if we were given a valid consistency-enforcing procedure
if sys.argv[3] == "none":
    backtrack()
elif sys.argv[3] == "fc":
    forwardCheck()
else:
    print('Invalid consistency-enforcing procedure.')
    closeFiles()
    exit()

closeFiles()