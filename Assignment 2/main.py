# Andrew Sylvester and Cameron Meyer
# CS 4365 - Assignment 2 part 2
# main.py

import sys
import os.path
import re

#Global vars
domains = {}        #Dictionary of variables, and their associated domain of values
constraints = []    #Array of tuples containing each constraint between variables
#chosenVars = []     #Array of tuples keeping track of the order of assigned variables, and their current associated value
varFile = None      #The .var input file
conFile = None      #The .con input file
branchNumber = 1

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
    global domains
    global constraints
    backtrackHelper(domains, constraints, [])

def backtrackHelper(workingDomains, workingConstraints, chosenVars):
    if len(workingDomains) == len(chosenVars): #We successfully assigned all variables then
        printBranch(chosenVars, 'solution')
        return True
    #domIndex = 0    #Domain index representing the current entry in the list of values possibl;e for a variable's domain
    #print('Chosen Vars so far: ', chosenVars)
    simpleChosenVars = []
    for touple in chosenVars:
        simpleChosenVars.append(touple[0])
    MCVar = mostConstrained(workingDomains, simpleChosenVars)
    #print('========')
    #print('Length of remaining domains for the variable \'', MCVar, '\': ', len(workingDomains[MCVar]))
    #print('Remaining domains for the variable \'', MCVar, '\': ', workingDomains[MCVar])
    currVarDomain = workingDomains[MCVar].copy()
    workingDomains[MCVar] = currVarDomain
    while len(currVarDomain) >= 1:
        currentValue = leastConstrainingValue(MCVar, workingDomains, simpleChosenVars)
        #print('Variable chosen: ',MCVar)
        #print('Current Value: ',currentValue)
        currVarDomain.remove(currentValue)
        #print('Working  Domain',workingDomains)
        failed = False
        assignment = (MCVar, currentValue)

        for currConstraint in constraints:
            constraintWorked = True
            if MCVar in currConstraint:
                if currConstraint[0] == MCVar and currConstraint[2] in simpleChosenVars: 
                    constraintWorked = False
                    for val in workingDomains[currConstraint[2]]:
                        if compareConstraint(currConstraint[1], currentValue, val):
                            constraintWorked = True
                            break
                elif currConstraint[2] == MCVar and currConstraint[0] in simpleChosenVars:
                    constraintWorked = False
                    for val in workingDomains[currConstraint[0]]:
                        if compareConstraint(currConstraint[1], val, currentValue):
                            constraintWorked = True
                            break
            if not constraintWorked:
                #print(currConstraint," did not work")
                failed = True
                break

        #domIndex = domIndex + 1
        newChosenVars = chosenVars.copy() #Probably need to make this a variable passed on each recursion
        newChosenVars.append(assignment)
                #Failed, try next index
        if failed:
            printBranch(newChosenVars, 'failure')
            #print('========')
            continue
        #Make a copy of domains without the current var to pass on
        newDomains = workingDomains.copy()
        newDomains[MCVar] = [assignment[1]]
        #newDomains.pop(MCVar) don't pop full variable, just want to reduce list
        #workingConstraints.pop()  #how to actually make sure we're removing the correct element here?
        if backtrackHelper(newDomains, workingConstraints, newChosenVars):
            return True
    return False #is this right?? how do we actually know if the backtrack returned successfully??

def forwardCheck():
    print(leastConstrainingValue('D', domains))

def mostConstrained(workingDomains, chosenVars):
    mostConList = []
    smallestDomain = 99
    #Find smallest domains
    for var in workingDomains:
        if var in chosenVars:
            continue
        if len(workingDomains[var]) < smallestDomain:
            mostConList = [var]
            smallestDomain = len(workingDomains[var])
        elif len(workingDomains[var]) == smallestDomain:
            mostConList.append(var)
    #Check if only one value, otherwise use most constraining
    if len(mostConList) == 1:
        return mostConList[0]
    else:
        return mostConstraining(mostConList, chosenVars)

def mostConstraining(valList, chosenVars): #Error here
    mostConst = 0
    mostConstVar = valList[0]
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

def leastConstrainingValue(var, domainsToCheck, chosenVars):
    possibleValues = {}
    varsAffected = []
    #Find variables that are constrained with var
    for constraint in constraints:
        if constraint[0] == var:
            if constraint[2] not in varsAffected and constraint[2] not in chosenVars:
                varsAffected.append(constraint[2])
        elif constraint[2] == var:
            if constraint[0] not in varsAffected and constraint[0] not in chosenVars:
                varsAffected.append(constraint[0])
    #print(varsAffected)
    #For each value in the domain of var compare it with the constraints and tally the total domain lengths for all affects variables.
    totalAmountAffected = []
    for value in domainsToCheck[var]:
        numTrue = 0
        for affectedVar in varsAffected:
            for affectedValue in domainsToCheck[affectedVar]:
                for constraint in constraints:
                    if affectedVar == constraint[0] and var == constraint[2]:
                        if(compareConstraint(constraint[1], affectedValue, value)):
                            numTrue += 1
                    elif affectedVar == constraint[2] and var == constraint[0]:
                        if(compareConstraint(constraint[1], value, affectedValue)):
                            numTrue += 1
        totalAmountAffected.append(numTrue)
    #print(totalAmountAffected)
    #Find the largest total (least constraining value)
    largestTotal = totalAmountAffected[0]
    lsv = 0
    for i in range(len(totalAmountAffected)):
        if totalAmountAffected[i] > largestTotal:
            largestTotal = totalAmountAffected[i]
            lsv = i
    return domainsToCheck[var][lsv]

def printBranch(chosenVars, endOfString):
    global branchNumber
    line = "" + str(branchNumber) + ". "
    branchNumber += 1
    for i in range(len(chosenVars)):
        if i < len(chosenVars) - 1:
            line = line + chosenVars[i][0] + "=" + str(chosenVars[i][1]) + ", "
        else:
            line = line + chosenVars[i][0] + "=" + str(chosenVars[i][1])
    print(line," ",endOfString)


def compareConstraint(operator, val1, val2):
    if operator == '<':
        return val1 < val2
    elif operator == '>':
        return val1 > val2
    elif operator == '=':
        return val1 == val2
    elif operator == '!':
        return not(val1 == val2)

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