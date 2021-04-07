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
clauseTotal = 0

#Functions
def negateClause(clause):
    for i in range(len(clause)):
        CNF = []
        CNF.append((clause[i][0],not clause[i][1]))
        #CNF.append([])
        KB.append(CNF)

#Iterate through KB and find resolutions. If found create new clause. If new clause would be empty contradiction is found.
def findNewClause():
    #print("Starting anew")
    clausei = 0
    KBSize = len(KB)
    while clausei < KBSize:
        for clausej in range(clausei):
            newClauseFound = False
            for x in range(len(KB[clausej])):
                for y in range(len(KB[clausei])):
                    if KB[clausei][y][0] == KB[clausej][x][0] and KB[clausei][y][1] != KB[clausej][x][1]:
                        #print(KB[clausei]," and ",KB[clausej]," can cancel.")
                        if len(KB[clausei]) == 1 and len(KB[clausej]) == 1:
                            KB.append([("Contradiction",False)])#, [clausei + 1, clausej + 1]])
                            printKB()
                            #print("Contradiction {" + str(clausei + 1) + ", " + str(clausej + 1) + "}")
                            return True #Contradiction found
                        newClauseFound = createNewClause(clausei, clausej, y, x)
                        #return findNewClause() #CHANGE FROM RECURSION TO LOOP
                        break
                if newClauseFound:
                    KBSize += 1
                    break
        clausei += 1
    #if not newClauseFound:
    printKB()
    return False #No contradiction found

#Create new clause from the two passed in clauses.                        
def createNewClause(clausei, clausej, commonLiterali, commonLiteralj):
    newClause = []
    #literals = []
    #negations = []
    #Get all literals from clause i
    for i in range(len(KB[clausei])):
        if i != commonLiterali:
            newClause.append((KB[clausei][i][0], KB[clausei][i][1]))
    #Get all unique literals from clause j
    for i in range(len(KB[clausej])):
        if i != commonLiteralj:
            if KB[clausej][i] in newClause:
                #print("Already in clause")
                continue
            #print("Adding literal from j")
            newClause.append(KB[clausej][i])
            #negations.append(KB[clausej][1][i])
    
    #newClause.append(literals)
    #newClause.append(negations)
    #newClause.append([clausei + 1, clausej + 1])
    #print("Creating new clause with: ",clausei + 1," ",clausej + 1,": ",newClause)
    #print("New clause created",newClause)
    duplicate = False
    #Check that it doesn't evaluate to true always
    for x in range(len(newClause)):
        for y in range(x, len(newClause)):
            if newClause[x][0] == newClause[y][0] and newClause[x][1] != newClause[y][1]:
                duplicate = True
                break
                #print("Is true always")
        if duplicate:
            break
    
    newClause.sort()
    if not duplicate:
        if newClause in KB:
            duplicate = True
    #print("Is already in KB: ",duplicate)
    global clauseTotal
    if not duplicate:
        KB.append(newClause)
        clauseTotal += 1
        print("New clause added",clauseTotal)
        #printKB()
        return True
    else:
        return False

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
        for i in range(len(clause)):
            if clause[i][1] == True:
                output += "~"
            output += clause[i][0]

            if i < len(clause) - 1:
                output += " "
        #output += " {"
        #for i in range(len(clause[2])):
        #    if i == len(clause[2]) - 1:
        #        output += str(clause[2][i])
        #    else:
        #        output += str(clause[2][i]) + ", "
        #output += "}"
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
        for i in range(len(literals)):
            CNF.append((literals[i], negations[i]))
        #CNF.append(literals)
        #CNF.append(negations)
        #CNF.append([])
        #print(CNF)
        CNF.sort()

        nextLine = inFile.readline()

        if not nextLine == "":
            KB.append(CNF)
            clauseTotal += 1
        else:
            #Final line is to be checked with resolution somehow, I don't think it goes in the KB??
            origClause = CNF

#testArray = [[[("a", False), ("b", True)], [1, 3]], [[("c", False), ("d", True)], [1, 2]]]
if ("a", False) == ("b", False):
    print("In array")

negateClause(origClause)
printKB()
if findNewClause(): #ADD current line number
    print("Valid")
else:
    print("Fail")
closeFiles()