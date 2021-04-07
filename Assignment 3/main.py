# Andrew Sylvester and Cameron Meyer
# CS 4365 - Assignment 3 part 1
# main.py

import sys
import os.path
import re
import array

#Global vars
inFile = None
KB = [] #A 3D array of the knowledge base. Access in the form KB[Clause][Literal][Var/Val]
        #There are n-1 clauses, 2 var/val options, and ?? number of literals
        #Each clause stores the literals as a tuple with the literal string and bool for if there is a ~. ~a = (a, True)
sortedKB = [] #Copy of KB but each clause is in alphabetical order. This is used to more optimally search for duplicate clauses.
origClause = None
clauseTotal = 1

#Functions
#Take the clause to test for and break it apart and negate it and add to the KB
def negateClause(clause):
    global KB
    global sortedKB
    for i in range(len(clause)):
        CNF = []
        CNF.append((clause[i][0],not clause[i][1]))
        sortedKB.append(CNF.copy())
        CNF.append((0,0))
        KB.append(CNF)
        printKBLine(CNF)

#Iterate through KB and find resolutions. If found create new clause. If new clause would be empty contradiction is found.
def findNewClause():
    clausei = 0
    KBSize = len(KB)
    while clausei < KBSize:
        for clausej in range(clausei):
            newClauseFound = False
            for x in range(len(KB[clausej]) - 1):
                for y in range(len(KB[clausei]) - 1):
                    if KB[clausei][y][0] == KB[clausej][x][0] and KB[clausei][y][1] != KB[clausej][x][1]:
                        if len(KB[clausei]) == 2 and len(KB[clausej]) == 2:
                            contradiction = [("Contradiction",False), (clausei + 1, clausej + 1)]
                            KB.append(contradiction)
                            printKBLine(contradiction)
                            return True #Contradiction found
                        newClauseFound = createNewClause(clausei, clausej, y, x)
                        break
                if newClauseFound:
                    KBSize += 1
                    break
        clausei += 1
    return False #No contradiction found

#Create new clause from the two passed in clauses.                        
def createNewClause(clausei, clausej, commonLiterali, commonLiteralj):
    newClause = []

    #Get all literals from clause i
    for i in range(len(KB[clausei]) - 1):
        if i != commonLiterali:
            newClause.append((KB[clausei][i][0], KB[clausei][i][1]))

    #Get all unique literals from clause j
    for i in range(len(KB[clausej]) - 1):
        if i != commonLiteralj:
            if KB[clausej][i] in newClause:
                continue
            newClause.append(KB[clausej][i])
    
    duplicate = False
    #Check that it doesn't evaluate to true always
    for x in range(len(newClause)):
        for y in range(x, len(newClause)):
            if newClause[x][0] == newClause[y][0] and newClause[x][1] != newClause[y][1]:
                duplicate = True
                break
        if duplicate:
            break

    #Create sorted copy for optimized search
    sortedNewClause = newClause.copy()
    sortedNewClause.sort()
    if not duplicate:
        if sortedNewClause in sortedKB:
            duplicate = True

    if not duplicate:
        newClause.append((clausei + 1, clausej + 1))
        KB.append(newClause)
        sortedKB.append(sortedNewClause)
        printKBLine(newClause)
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

#Prints whole KB. Not currently being used in the program as we opted to print each line seperatly as we find a new clause.
def printKB():
    global KB
    line = 1
    for clause in KB:
        output = str(line) + ". "
        for i in range(len(clause) - 1):
            if clause[i][1] == True:
                output += "~"
            output += clause[i][0]

            if i < len(clause) - 2:
                output += " "
        if clause[len(clause) - 1][0] == 0:
            output += " {}"
        else:
            output += " {" + str(clause[len(clause) - 1][0]) + ", " + str(clause[len(clause) - 1][1]) + "}"

        #for i in range(len(clause[2])):
        #    if i == len(clause[2]) - 1:
        #        output += str(clause[2][i])
        #    else:
        #        output += str(clause[2][i]) + ", "
        #output += "}"
        print(output)
        line += 1

#Print the current clause.
def printKBLine(clause):
    global KB
    global clauseTotal
    output = str(clauseTotal) + ". "
    clauseTotal += 1
    for i in range(len(clause) - 1):
        if clause[i][1] == True:
            output += "~"
        output += clause[i][0]

        if i < len(clause) - 2:
            output += " "
    if clause[len(clause) - 1][0] == 0:
        output += " {}"
    else:
        output += " {" + str(clause[len(clause) - 1][0]) + ", " + str(clause[len(clause) - 1][1]) + "}"
    print(output)

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
        
        #Copy and sort clause
        sortedCNF = CNF.copy()
        sortedCNF.sort()

        nextLine = inFile.readline()

        if not nextLine == "":
            CNF.append((0,0))
            KB.append(CNF)
            sortedKB.append(sortedCNF)
            printKBLine(CNF)
        else:
            #Final line is to be checked with resolution somehow, I don't think it goes in the KB??
            origClause = CNF

negateClause(origClause)

if findNewClause():
    print("Valid")
else:
    print("Fail")
closeFiles()