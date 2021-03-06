# Andrew Sylvester and Cameron Meyer
# CS 4365 - Assignment 1 part 2
# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from game import Directions
    n = Directions.NORTH
    e = Directions.EAST
    s = Directions.SOUTH
    w = Directions.WEST
    fail = Directions.STOP

    from util import Queue
    from util import Stack
    succ = problem.getSuccessors(problem.getStartState())
    allSuccessors = Stack()

    for element in succ:
        allSuccessors.push(element)
    path = Stack()
    hasBeenTo = [problem.getStartState()]

    while not allSuccessors.isEmpty():
        node = allSuccessors.pop()
        path.push(node)
        #print("Node pushed:", node)
        hasBeenTo.append(node[0])

        #check if the current node is the goal node, returning the directions if so
        if problem.isGoalState(node[0]):
            directions = []
            while not path.isEmpty():
                directions.insert(0, path.pop()[1]) 
            #print("Goal Found with path:", directions)
            return directions

        newSuccessors = 0   #the number of successors to this node that have not yet been visited
        backtracked = False #whether we hit a dead end in DFS and are backtracking to an earlier node

        #backtrack as needed until there is a new successor to check
        while newSuccessors == 0 and not path.isEmpty():
            S = problem.getSuccessors(node[0])
            for element in S:
                if not element[0] in hasBeenTo:
                    newSuccessors += 1

                    #we backtracked to find a node with valid successors but already removed it from the path. adding it back here
                    if backtracked and newSuccessors == 1:
                        path.push(node)
                        #print("Node pushed:", node)
                    elif not backtracked:
                        allSuccessors.push(element)

            #backtrack to an earlier node if there's no valid paths from here
            if newSuccessors == 0:
                node = path.pop()
                #print("Node popped:", node)
                backtracked = True

    return  [fail]

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from game import Directions
    fail = Directions.STOP

    from util import Queue
    from util import Stack
    succ = problem.getSuccessors(problem.getStartState())
    allSuccessors = Queue()
    allPaths = Queue() #A queue of lists for a path of each function.

    
    hasBeenTo = [problem.getStartState()]

    for element in succ:
        allSuccessors.push(element)
        allPaths.push([element[1]])
        hasBeenTo.append(element[0])
        
    while not allSuccessors.isEmpty():
        node = allSuccessors.pop()
        parentPath = allPaths.pop()
        #hasBeenTo.append(node[0])

        #check if the current node is the goal node, returning the directions if so
        if problem.isGoalState(node[0]):
            return parentPath

        #Add Successors if not found already
        S = problem.getSuccessors(node[0])
        for element in S:
            if not element[0] in hasBeenTo:
                allSuccessors.push(element)
                hasBeenTo.append(element[0])
                newPath = parentPath.copy()
                newPath.append(element[1])
                allPaths.push(newPath) 

    return  [fail]

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from game import Directions
    fail = Directions.STOP

    from util import Queue
    from util import PriorityQueue
    from util import Stack
    succ = problem.getSuccessors(problem.getStartState())
    allSuccessors = PriorityQueue()
    allPaths = PriorityQueue() #A queue of lists for a path of each function.
    allPathsCost = PriorityQueue()
    
    hasExpanded = [problem.getStartState()]

    for element in succ:
        allSuccessors.push(element, element[2])
        allPaths.push([element[1]], element[2])
        allPathsCost.push(element[2], element[2])
        
    while not allSuccessors.isEmpty():
        node = allSuccessors.pop()
        parentPath = allPaths.pop()
        pathCost = allPathsCost.pop()
        if not node[0] in hasExpanded:
            #print("Node is ", node)

            hasExpanded.append(node[0])

            #check if the current node is the goal node, returning the directions if so
            if problem.isGoalState(node[0]):
                return parentPath

            #Add Successors if not found already
            S = problem.getSuccessors(node[0])
            for element in S:
                if not element[0] in hasExpanded:
                    g = pathCost + element[2]
                    allSuccessors.push(element, g)
                    newPath = parentPath.copy()
                    newPath.append(element[1])
                    allPaths.push(newPath, g) 
                    allPathsCost.push(g, g)

    return  [fail]

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from game import Directions
    fail = Directions.STOP

    from util import Queue
    from util import PriorityQueue
    from util import Stack
    succ = problem.getSuccessors(problem.getStartState())
    allSuccessors = PriorityQueue()
    allPaths = PriorityQueue() #A queue of lists for a path of each function.
    allPathsGCost = PriorityQueue()
    
    hasExpanded = [problem.getStartState()]

    for element in succ:
        allSuccessors.push(element, element[2] + heuristic(element[0], problem))
        allPaths.push([element[1]], element[2] + heuristic(element[0], problem))
        allPathsGCost.push(element[2], element[2] + heuristic(element[0], problem))
        
    while not allSuccessors.isEmpty():
        node = allSuccessors.pop()
        parentPath = allPaths.pop()
        pathCost = allPathsGCost.pop()
        if not node[0] in hasExpanded:
            #print("Node is ", node)

            hasExpanded.append(node[0])

            #check if the current node is the goal node, returning the directions if so
            if problem.isGoalState(node[0]):
                return parentPath

            #Add Successors if not found already
            S = problem.getSuccessors(node[0])
            for element in S:
                if not element[0] in hasExpanded:
                    g = pathCost + element[2]
                    f = g + heuristic(element[0], problem)
                    allSuccessors.push(element, f)
                    newPath = parentPath.copy()
                    newPath.append(element[1])
                    allPaths.push(newPath, f) 
                    allPathsGCost.push(g, f)

    return  [fail]


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
