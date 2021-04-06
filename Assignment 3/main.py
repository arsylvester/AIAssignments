# Andrew Sylvester and Cameron Meyer
# CS 4365 - Assignment 3 part 1
# main.py

import sys
import os.path
import re
import array

#Global vars
inFile = None
KB = [] #A 3D array of the knowledge base. Access in the form KB[Clause][Var/Val][Literal]
        #There are n-1 clauses, 2 var/val options, and ?? number of literals
origClause = None

#Functions
def negateClause(clause):
    for i in range(len(clause[0])):
        CNF = []
        CNF.append([clause[0][i]])
        CNF.append([not clause[1][i]])
        CNF.append([])
        KB.append(CNF)

def findNewClause():
    for clausei in reversed(range(len(KB))):
        newClauseFound = False
        for clausej in range(clausei):
            for x in range(len(KB[clausej][0])):
                for y in range(len(KB[clausei][0])):
                    if KB[clausei][0][y] == KB[clausej][0][x] and KB[clausei][1][y] != KB[clausej][1][x]:
                        #print(KB[clausei]," and ",KB[clausej]," can cancel.")
                        if len(KB[clausei][0]) == len(KB[clausej][0]):
                            printKB()
                            print("Contradiction {" + str(clausei + 1) + ", " + str(clausej + 1) + "}")
                            return True #Contradiction found
                        createNewClause(clausei, clausej, y, x)
                        return findNewClause()
                        newClauseFound = True
                        break
    return False #No contradiction found
                        
def createNewClause(clausei, clausej, commonLiterali, commonLiteralj):
    newClause = []
    literals = []
    negations = []
    for i in range(len(KB[clausei][0])):
        if KB[clausei][0][i] != KB[clausei][0][commonLiterali]: #STILL NEED TO CHECK FOR DUPLICATES
            literals.append(KB[clausei][0][i])
            negations.append(KB[clausei][1][i])
    for i in range(len(KB[clausej][0])):
        if KB[clausej][0][i] != KB[clausej][0][commonLiteralj]: #STILL NEED TO CHECK FOR DUPLICATES
            literals.append(KB[clausej][0][i])
            negations.append(KB[clausej][1][i])

    newClause.append(literals)
    newClause.append(negations)
    newClause.append([clausei + 1, clausej + 1])
    KB.append(newClause)

#Attempt to open files, return true if successful
def openFiles():
    #Check if the given inFile file exists
    if(os.path.isfile(sys.argv[1])):
        global inFile
        inFile = open(sys.argv[1], "r")
    else:
        print('inFile file does not exist.')
        return False

    #The files were successfully opened
    return True

def closeFiles():
    #Close files as needed
    if(not inFile == None):
        inFile.close()

def printKB():
    global KB
    line = 1
    for clause in KB:
        output = str(line) + ". "
        for i in range(len(clause[0])):
            if clause[1][i] == True:
                output += "~"
            output += clause[0][i]

            if i < len(clause[0]) - 1:
                output += " "
        output += " {"
        for i in range(len(clause[2])):
            if i == len(clause[2]) - 1:
                output += str(clause[2][i])
            else:
                output += str(clause[2][i]) + ", "
        output += "}"
        print(output)
        line += 1

#Include logic for reading command line, files, and main processes here.
#Check for exact number of command line arguments
if not len(sys.argv) == 2:
    print('Invalid number of arguments. Searching for 1 arguments and found ', len(sys.argv) - 1, '.') #Looking for 1 arg besides the python filename
    exit()

if not openFiles():   
    exit()

#Check if the inFile file is open
if not inFile == None:
    #Read in each line of data to an array and remove unnecessary characters
    nextLine = inFile.readline()
    while(not nextLine == ""):
        literals = re.split("[ \n]", nextLine)
        emptyCount = literals.count('')
        for i in range(emptyCount):
            literals.remove('')

        negations = []

        for i in range(len(literals)):
            if literals[i].find("~") == 0:
                negations.append(True)
                literals[i] = literals[i][1:]
            else:
                negations.append(False)

        CNF = []
        CNF.append(literals)
        CNF.append(negations)
        CNF.append([])
        #print(CNF)

        nextLine = inFile.readline()

        if not nextLine == "":
            KB.append(CNF)
        else:
            #Final line is to be checked with resolution somehow, I don't think it goes in the KB??
            origClause = CNF

negateClause(origClause)
if findNewClause():
    print("Valid")
else:
    print("Not Valid")
closeFiles()