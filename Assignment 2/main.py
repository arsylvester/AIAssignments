#Global vars
domain = {
    'X': [0, 1, 2],
    'Y': [0, 1, 2],
    'Z': [1, 2]
}
constraints = [('X', '=', 'Z'), ('X', '<', 'Y')]
chosenVars = []

#Functions
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
    return "Var"

def alphabetical(valLists):
    return "Var"

#Include logic for reading command line, files, and main processes here.
backtrack()