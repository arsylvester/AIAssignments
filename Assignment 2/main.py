# Andrew Sylvester and Cameron Meyer
# CS 4365 - Assignment 2 part 2
# main.py

import sys
import os.path
import re

#Global vars
domain = {}
constraints = [('Y', '=', 'Z'), ('X', '<', 'Y')]
chosenVars = []
varFile = None
conFile = None

#Functions
def assignDomain():
    global varFile
    if not varFile == None:
        line = re.split("[ :\n]", varFile.readline())
        emptyCount = line.count('')
        for i in range(emptyCount):
            line.remove('')
        variable = line[0]
        line.remove(line[0])

        numbers = []
        for num in line:
            numbers.append(int(num))
        domain.update({variable : numbers})

def backtrack():
    print(mostConstrained())

def forwardCheck():
    print("ForwardChecking")

def mostConstrained():
    mostConList = []
    smallestDomain = 99
    #Find smallest domains
    for var in domain:
        if len(domain[var]) < smallestDomain:
            mostConList = [var]
            smallestDomain = len(domain[var])
        elif len(domain[var]) == smallestDomain:
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
        confile = open(sys.argv[2], "r")
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