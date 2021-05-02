# myTeam.py
# Pacman agent developed by Andrew Sylvester and Cameron Meyer for CS 4365.001.
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


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveNamcapAgent', second = 'DefensiveTsohgAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class NamcapCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """
 
  def registerInitialState(self, gameState):
    self.start = gameState.getAgentPosition(self.index)
    self.pelletLimit = len(self.getFood(gameState).asList()) - 2 #Pellet limit that when reached the agents will return to their side. Value hardcoded for now
    CaptureAgent.registerInitialState(self, gameState)
    self.halfwayPoint = len(gameState.getRedFood()[0])
    self.verticalHalfwayPoint = len(gameState.getRedFood()[1]) /2
    self.fleeing = False
    #print(len(gameState.getRedFood()[0]))
    #print(gameState.getAgentState(self.index).getPosition())

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights
    """
    Looks something like this
    -2034
    feature = {'distanceToFood': 35, 'successorScore': -20}
    weights = {'distanceToFood': -1, 'successorScore': 100}
    """
    

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}

class OffensiveNamcapAgent(NamcapCaptureAgent):
  """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """
  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    Given a state s and set of actions a, this agent will select an action that will help maximize the reward score for performing an action in that state. 
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions] # Determine how many points each action is worth (for all legal actions that can be performed)
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values) # Determine the best possible score for any action
    bestActions = [a for a, v in zip(actions, values) if v == maxValue] # Keep track of every possible action with the highest possible score

    foodLeft = len(self.getFood(gameState).asList())

    #print(self.fleeing)
    if foodLeft <= self.pelletLimit: # Agent will not return until all but two pellets are eaten
      #currentPos = gameState.getAgentPosition(self.index)
      if not gameState.getAgentState(self.index).isPacman: #If we scored this turn, go back for more points
        self.pelletLimit -= 2
        self.fleeing = False
      else:
        self.fleeing = True
    else:
      self.fleeing = False
    '''
      #elif(gameState.getAgentPosition(self.index) <)
      bestDist = 9999
      #print("Is returning to our side")
      for action in actions:
        successor = self.getSuccessor(gameState, action)
        pos2 = successor.getAgentPosition(self.index) # Keep track of where this action will put me on the map
        dist = self.getMazeDistance(self.start,pos2)  # Keep track of the distance between this action's location and the spawn location
                                                      # This could be updated to just be shortest path to anywhere on your own side!
        if dist < bestDist: # Take the shortest path from here to spawn
          bestAction = action
          bestDist = dist
      return bestAction
    '''

    return random.choice(bestActions)
  """
  This function finds the amount of food left and the distance to food. 
  The closer a action is to food the lower the cost, and if an action recieves a pellet, drastically reduce the cost of the next action
  """
  def getFeatures(self, gameState, action):
    #print(self.getScore(gameState)) 
    if(self.getScore(gameState) < 2):
      features = util.Counter()
      successor = self.getSuccessor(gameState, action)
      foodList = self.getFood(successor).asList()    
      #self.getScore(successor)

      if self.fleeing: # Agent will not return until all but two pellets are eaten
        myPos = successor.getAgentPosition(self.index)

        minDistance = 1000000
        for i in range(len(gameState.getRedFood()[1])):
          hwp = self.halfwayPoint
          if self.red:
            hwp -= 1
          else:
            hwp += 1
          if not gameState.hasWall(hwp, i):
            manhattanDist = self.getMazeDistance(myPos, (hwp, i))
            minDistance = min(minDistance, manhattanDist)

        features['distanceToBase'] = minDistance
        if(not successor.getAgentState(self.index).isPacman):
          features['successorScore'] = 1
      else:
        features['successorScore'] = -len(foodList)
        # Compute distance to the nearest food
        if len(foodList) > 0: # This should always be True,  but better safe than sorry
          myPos = successor.getAgentState(self.index).getPosition()
          minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
          features['distanceToFood'] = minDistance

      # Computes distance to Ghosts we can see
      enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
      ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]
      if len(ghosts) > 0 and successor.getAgentState(self.index).isPacman:
        dists = [self.getMazeDistance(myPos, a.getPosition()) for a in ghosts]
        features['distanceToEnemyGhost'] = min(dists)

      """
      #If action leads to a ghost don't go that way
      #print(successor.getAgentPosition(self.getOpponents(gameState)[0]))
      opponentList = self.getOpponents(gameState)
      for x in range(len(opponentList)):
        myPos = successor.getAgentState(self.index).getPosition()
        if(successor.getAgentPosition(self.getOpponents(gameState)[x]) == myPos):
          features['isGhost'] = -1
      """

      return features
    else:
      return self.getFeaturesDef(gameState, action)

  def getFeaturesDef(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0). This really just checks if we are on our side or not.
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0 

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)
    else: #If no enemy pacman on our side, stay in the close third towards the center. TODO: If both agents are on defense, on go north and one stay south.
      if (self.red and action == Directions.WEST) or (not self.red and action == Directions.EAST):
        closeThird = self.halfwayPoint / 2
        if(self.red and myPos[0] <= self.halfwayPoint - closeThird) or (not self.red and myPos[0] > self.halfwayPoint + closeThird):
          features['centerDistance'] = 1
      teamMate = self.getTeam(gameState)[0]
      if teamMate == self.index:
        teamMate = self.getTeam(gameState)[1]
      if not successor.getAgentState(teamMate).isPacman and self.getScore(successor) > 0: #If both ghosts playing defense
        if myPos[1] > self.verticalHalfwayPoint:
          features['stayTop'] = 1

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    if(self.getScore(gameState) >= 2):
      return self.getWeightsDef(gameState, action)
    else:
      return {'successorScore': 100, 'distanceToFood': -2, 'isGhost': 1000, 'distanceToEnemyGhost': 1, 'distanceToBase': -2}

  def getWeightsDef(self, gameState, action):
    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2, 'centerDistance': -5, 'stayTop': -2} 

class DefensiveTsohgAgent(NamcapCaptureAgent):
  """
  A reflex agent that keeps its side Pacman-free. Again,
  this is to give you an idea of what a defensive agent
  could be like.  It is not the best or only way to make
  such an agent.
  """

  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    Given a state s and set of actions a, this agent will select an action that will help maximize the reward score for performing an action in that state. 
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions] # Determine how many points each action is worth (for all legal actions that can be performed)
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values) # Determine the best possible score for any action
    bestActions = [a for a, v in zip(actions, values) if v == maxValue] # Keep track of every possible action with the highest possible score

    return random.choice(bestActions)

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0). This really just checks if we are on our side or not.
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0 

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)
    else: #If no enemy pacman on our side, stay in the close third towards the center. TODO: If both agents are on defense, on go north and one stay south.
      if (self.red and action == Directions.WEST) or (not self.red and action == Directions.EAST):
        closeThird = self.halfwayPoint / 3
        if(self.red and myPos[0] <= self.halfwayPoint - closeThird) or (not self.red and myPos[0] > self.halfwayPoint + closeThird):
          features['centerDistance'] = 1
      teamMate = self.getTeam(gameState)[0]
      if teamMate == self.index:
        teamMate = self.getTeam(gameState)[1]
      if not successor.getAgentState(teamMate).isPacman and self.getScore(successor) > 0: #If both ghosts playing defense
        if myPos[1] < self.verticalHalfwayPoint:
          features['stayTop'] = 1
          

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2, 'centerDistance': -5, 'stayTop': -2}

class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''


  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)

    '''
    You should change this in your own agent.
    '''

    return random.choice(actions)

