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
    backtrackHelper(domains, [])

def backtrackHelper(workingDomains, chosenVars):
    if len(workingDomains) == len(chosenVars): #We successfully assigned all variables then (Base case)
        printBranch(chosenVars, 'solution')
        return True

    #Need a simple version for mostConstrained and leastConstrainingValue
    simpleChosenVars = []
    for touple in chosenVars:
        simpleChosenVars.append(touple[0])
    MCVar = mostConstrained(workingDomains, simpleChosenVars)

    #Python and Dictionaries are weird, so have to do this so that we don't overwrite information higher in the recursion tree.
    currVarDomain = workingDomains[MCVar].copy()
    workingDomains[MCVar] = currVarDomain

    #loop till all values in the domain have been tried
    while len(currVarDomain) >= 1:
        #Find leastConstraingValue
        currentValue = leastConstrainingValue(MCVar, workingDomains, simpleChosenVars)
        currVarDomain.remove(currentValue)
        failed = False
        assignment = (MCVar, currentValue)

        #Loop through contraints, if a constraint is affected by a var check it with already assigned variables to see if it fails.
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
        
        #Copy chosenVars with our current var appended to it to pass on
        newChosenVars = chosenVars.copy() 
        newChosenVars.append(assignment)
        #Failed, try next index
        if failed:
            printBranch(newChosenVars, 'failure')
            continue

        #Make a copy of domains without the current var to pass on
        newDomains = workingDomains.copy()
        newDomains[MCVar] = [assignment[1]]

        #Recursively call backtrack
        if backtrackHelper(newDomains, newChosenVars):
            return True
    return False 

def forwardCheck():
    global domains
    forwardCheckHelper(domains, [])

def forwardCheckHelper(workingDomains, chosenVars):
    if len(workingDomains) == len(chosenVars): #We successfully assigned all variables then (Base case)
        printBranch(chosenVars, 'solution')
        return True

    #Need a simple version for mostConstrained and leastConstrainingValue
    simpleChosenVars = []
    for touple in chosenVars:
        simpleChosenVars.append(touple[0])
    MCVar = mostConstrained(workingDomains, simpleChosenVars)

    #Python and Dictionaries are weird, so have to do this so that we don't overwrite information higher in the recursion tree.
    currVarDomain = workingDomains[MCVar].copy()
    workingDomains[MCVar] = currVarDomain
    currentDomainsCopy = workingDomains.copy()

    #loop till all values in the domain have been tried
    while len(currVarDomain) >= 1:
        #Find leastConstraingValue
        currentValue = leastConstrainingValue(MCVar, workingDomains, simpleChosenVars)
        currVarDomain.remove(currentValue)
        failed = False
        assignment = (MCVar, currentValue)
        workingDomains = currentDomainsCopy.copy()


        #Loop through contraints, if a constraint is affected by a var check it with already assigned variables to see if it fails.
        for currConstraint in constraints:
            constraintWorked = True
            if MCVar in currConstraint:
                if currConstraint[0] == MCVar:
                    otherVarDomain = workingDomains[currConstraint[2]].copy()
                    workingDomains[currConstraint[2]] = otherVarDomain
                    constraintWorked = False
                    valuesToRemove = []
                    for val in workingDomains[currConstraint[2]]:
                        if compareConstraint(currConstraint[1], currentValue, val):
                            constraintWorked = True
                        else:
                            valuesToRemove.append(val)
                    for valToRemove in valuesToRemove:
                        otherVarDomain.remove(valToRemove)
                elif currConstraint[2] == MCVar:
                    otherVarDomain = workingDomains[currConstraint[0]].copy()
                    workingDomains[currConstraint[0]] = otherVarDomain
                    constraintWorked = False
                    valuesToRemove = []
                    for val in workingDomains[currConstraint[0]]:
                        if compareConstraint(currConstraint[1], val, currentValue):
                            constraintWorked = True
                        else:
                            valuesToRemove.append(val)
                    for valToRemove in valuesToRemove:
                        otherVarDomain.remove(valToRemove)
            if not constraintWorked:
                failed = True
                break
        
        #Copy chosenVars with our current var appended to it to pass on
        newChosenVars = chosenVars.copy() 
        newChosenVars.append(assignment)
        #Failed, try next index
        if failed:
            printBranch(newChosenVars, 'failure')
            continue

        #Make a copy of domains without the current var to pass on
        newDomains = workingDomains.copy()
        newDomains[MCVar] = [assignment[1]]

        #Recursively call backtrack
        if forwardCheckHelper(newDomains, newChosenVars):
            return True
    return False 


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
    #Find the largest total (least constraining value)
    largestTotal = totalAmountAffected[0]
    lcv = 0
    for i in range(len(totalAmountAffected)):
        if totalAmountAffected[i] > largestTotal:
            largestTotal = totalAmountAffected[i]
            lcv = i
    return domainsToCheck[var][lcv]

def printBranch(chosenVars, endOfString):
    global branchNumber
    line = "" + str(branchNumber) + ". "
    branchNumber += 1
    for i in range(len(chosenVars)):
        if i < len(chosenVars) - 1:
            line = line + chosenVars[i][0] + "=" + str(chosenVars[i][1]) + ", "
        else:
            line = line + chosenVars[i][0] + "=" + str(chosenVars[i][1])
    print(line,"",endOfString)


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