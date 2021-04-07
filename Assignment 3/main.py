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

#Iterate through KB and find resolutions. If found create new clause. If new clause would be empty contradiction is found.
def findNewClause():
    while True:
        newClauseFound = False
        for clausei in range(len(KB)):
            for clausej in range(clausei):
                for x in range(len(KB[clausej][0])):
                    for y in range(len(KB[clausei][0])):
                        if KB[clausei][0][y] == KB[clausej][0][x] and KB[clausei][1][y] != KB[clausej][1][x]:
                            #print(KB[clausei]," and ",KB[clausej]," can cancel.")
                            if len(KB[clausei][0]) == 1 and len(KB[clausej][0]) == 1:
                                KB.append([["Contradiction"], [False], [clausei + 1, clausej + 1]])
                                printKB()
                                #print("Contradiction {" + str(clausei + 1) + ", " + str(clausej + 1) + "}")
                                return True #Contradiction found
                            newClauseFound = createNewClause(clausei, clausej, y, x)
                            #return findNewClause() #CHANGE FROM RECURSION TO LOOP
                            break
                    if newClauseFound:
                        break
                if newClauseFound:
                    break
            if newClauseFound:
                break
        if not newClauseFound:
            return False #No contradiction found

#Create new clause from the two passed in clauses.                        
def createNewClause(clausei, clausej, commonLiterali, commonLiteralj):
    newClause = []
    literals = []
    negations = []
    #Get all literals from clause i
    for i in range(len(KB[clausei][0])):
        if i != commonLiterali:
            literals.append(KB[clausei][0][i])
            negations.append(KB[clausei][1][i])
    #Get all unique literals from clause j
    for i in range(len(KB[clausej][0])):
        if i != commonLiteralj:
            isDup = False
            for x in range(len(literals)):
                if KB[clausej][0][i] == literals[x] and KB[clausej][1][i] == negations[x]:
                    #print("Already in clause")
                    isDup = True
                    break
            if isDup:
                continue
            #print("Adding literal from j")
            literals.append(KB[clausej][0][i])
            negations.append(KB[clausej][1][i])
    
    newClause.append(literals)
    newClause.append(negations)
    newClause.append([clausei + 1, clausej + 1])
    #print("Creating new clause with: ",clausei + 1," ",clausej + 1,": ",newClause)
    #print("New clause created",newClause)
    duplicate = False
    #Check that clause is not already in the KB
    for clauses in range(len(KB)):
        if(len(literals) == len(KB[clauses][0])):
            clauseDup = True
            for i in range(len(literals)):
                literalDup = False
                for j in range(len(KB[clauses][0])):
                    if literals[i] == KB[clauses][0][j] and negations[i] == KB[clauses][1][j]:
                        literalDup = True
                        #print(literals[i]," is dup of ", KB[clauses][0][j]," and ", negations[i]," with ",KB[clauses][1][j])
                        break
                if not literalDup:
                    clauseDup = False
                    break
            if clauseDup:
                duplicate = True
    #print("Is already in KB: ",duplicate)

    #Check that it doesn't evaluate to true always
    if not duplicate:
        for x in range(len(literals)):
            for y in range(len(literals) - x - 1, len(literals)):
                if literals[x] == literals[y] and negations[x] != negations[y]:
                    duplicate = True
                    #print("Is true always")
    if not duplicate:
        KB.append(newClause)
        #print("New clause added",newClause)
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
if findNewClause(): #ADD current line number
    print("Valid")
else:
    print("Fail")
closeFiles()