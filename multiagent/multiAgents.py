# multiAgents.py
# --------------
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


#from asyncio.windows_events import NULL
NULL = None
from json.encoder import INFINITY
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        capsuleList = successorGameState.getCapsules()

        from util import manhattanDistance

        # print("successorState\n--------------------------------------------\n")
        # print(successorGameState)
        # print("successor Pos\n--------------------------------------------\n")
        # print(newPos)
        # print("newFood\n--------------------------------------------\n")
        # print(newFood)
        # print("sucessorGhostStates\n--------------------------------------------\n")
        # print(newGhostStates)
        # print("scaredTimes\n--------------------------------------------\n")
        # print(newScaredTimes)
        # print("\n\n")

        foodList = newFood.asList()
        foodDistanceList = []
        ghostDistanceList = []
        score = 0

        for pellet in foodList:
            foodDistanceList.append(manhattanDistance(newPos,pellet))

        for i in foodDistanceList:
            if i == 0:
                score += 5
                continue
            score += 5/i

        for ghost in successorGameState.getGhostPositions():
            ghostDistanceList.append(manhattanDistance(ghost,newPos))

        timeNumber = 0
        for time in newScaredTimes:
            if time > timeNumber:
                timeNumber = time
        # print("TimeNumber = ", timeNumber)

        
        for capsule in capsuleList:
            distanceToCapsule = manhattanDistance(newPos, capsule)
            if distanceToCapsule == 0:
                score += 2
                continue
            score += 2/distanceToCapsule

        for ghost in successorGameState.getGhostPositions():
            distanceToGhost = manhattanDistance(ghost, newPos)
            if timeNumber == 0:
                if distanceToGhost == 0:
                    score = 2 - score

                elif distanceToGhost <= 3:
                    score = 1 - score

            elif timeNumber > 0:
                if distanceToGhost == 0:
                    score += 1
                    continue
                score += 1/distanceToGhost
            
        # print("------SCORE: ", score)

        return successorGameState.getScore() + score


        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def maxValue(state, depth):

            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            
            elif depth == self.depth:
                value = self.evaluationFunction(state)
                # print("VALUE: ", value)
                return value

            bestMax = -INFINITY
            bestAction = NULL

            for action in state.getLegalActions(0):
                tempValue = minValue(state.generateSuccessor(0, action), 0 + 1, depth)
                if tempValue > bestMax:
                    bestAction = action
                    bestMax = tempValue
                    
            if depth == 0:
                # print("VALUE: ", bestMax)
                return bestAction
            return bestMax
        
        def minValue(state, agent, depth):
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            bestMin = INFINITY
            tempMin = 0
            nextAgent = agent + 1

            if agent == state.getNumAgents() - 1:
                nextAgent = 0
                   
            for action in state.getLegalActions(agent):
                agentState = state.generateSuccessor(agent, action)

                if nextAgent == 0:
                    tempMin = maxValue(agentState, depth + 1)
                
                else:
                    tempMin = minValue(agentState, nextAgent, depth)
                    
                if tempMin < bestMin:
                    bestMin = tempMin

            return bestMin
        
        value = maxValue(gameState, 0)
        # print("VALUE: ", value)
        return value

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        def maxValue(state, depth, alpha, beta):

            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            
            elif depth == self.depth:
                value = self.evaluationFunction(state)
                # print("VALUE: ", value)
                return value

            bestMax = -INFINITY
            bestAction = NULL

            for action in state.getLegalActions(0):
                tempValue = minValue(state.generateSuccessor(0, action), 0 + 1, depth, alpha, beta)
                if tempValue > bestMax:
                    bestAction = action
                    bestMax = tempValue
                    
                alpha = max(alpha, bestMax)
                if bestMax > beta:
                    return bestMax
            if depth == 0:
                # print("VALUE: ", bestMax)
                return bestAction
            return bestMax
        
        def minValue(state, agent, depth, alpha, beta):
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            bestMin = INFINITY
            tempMin = 0
            nextAgent = agent + 1

            if agent == state.getNumAgents() - 1:
                nextAgent = 0
                   
            for action in state.getLegalActions(agent):
                agentState = state.generateSuccessor(agent, action)

                if nextAgent == 0:
                    tempMin = maxValue(agentState, depth + 1, alpha, beta)
                
                else:
                    tempMin = minValue(agentState, nextAgent, depth, alpha, beta)
                    
                if tempMin < bestMin:
                    bestMin = tempMin
                beta = min(beta, bestMin)
                if bestMin < alpha:
                    return bestMin
            return bestMin
        value = maxValue(gameState, 0, -INFINITY, INFINITY)
        # print("VALUE: ", value)
        return value

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def maxValue(state, depth):

            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            
            elif depth == self.depth:
                value = self.evaluationFunction(state)
                # print("VALUE: ", value)
                return value

            bestMax = -INFINITY
            bestAction = NULL

            for action in state.getLegalActions(0):
                tempValue = probValue(state.generateSuccessor(0, action), 0 + 1, depth)
                if tempValue > bestMax:
                    bestAction = action
                    bestMax = tempValue
                
            if depth == 0:
                # print("VALUE: ", bestMax)
                return bestAction
            return bestMax
        
        def probValue(state, agent, depth):
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            tempValue = 0
            nextAgent = agent + 1

            if agent == state.getNumAgents() - 1:
                nextAgent = 0
                   
            for action in state.getLegalActions(agent):
                agentState = state.generateSuccessor(agent, action)

                if nextAgent == 0:
                    tempValue += maxValue(agentState, depth + 1)
                
                else:
                    tempValue += probValue(agentState, nextAgent, depth)
                    
            return tempValue * 1/len(state.getLegalActions(agent))
        value = maxValue(gameState, 0)
        # print("VALUE: ", value)
        return value

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
  
    score = currentGameState.getScore()
    pacmanPos = currentGameState.getPacmanPosition()
    ghosts = currentGameState.getGhostStates()
    food = currentGameState.getFood().asList()
    capsules = currentGameState.getCapsules()
    
    score -= 5 * len(food)
    for pellet in food:
        foodDistance = manhattanDistance(pacmanPos, pellet)
        if foodDistance < 3:
            score -= foodDistance
            continue
        score -= 0.35 * foodDistance
    
    score -= 15 * len(capsules)
    for capsule in capsules:
        distanceToCapsule = manhattanDistance(pacmanPos, capsule)
        if distanceToCapsule < 3:
            score -= 15 * distanceToCapsule
            continue
        score -= 10 * distanceToCapsule

    for ghost in ghosts:
        distanceToGhost = manhattanDistance(ghost.getPosition(), pacmanPos)
        if ghost.scaredTimer == 0:
            if distanceToGhost < 3:
                score += 4 * distanceToGhost
                continue
            score += distanceToGhost

        else:
            if distanceToGhost < 3:
                score -= 15 * distanceToGhost
                continue
            score -= 10 * distanceToGhost

    return score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
