#Include logic for reading command line, files, and main processes here.
domain = {
    'X': [0, 1, 2],
    'Y': [0, 1, 2],
    'Z': [1, 2]
}
constraints = [('X', '=', 'Z'), ('X', '<', 'Y')]
chosenVars = []

#Functions
def backtrack():
    print("Backtracking")

def forwardCheck():
    print("ForwardChecking")

def mostConstrained():
    return "Var"

def mostConstraining(valList):
    return "Var"

def alphabetical(valLists):
    return "Var"