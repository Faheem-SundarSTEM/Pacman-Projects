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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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

    def evaluationFunction(self, currentGameState: GameState, action):
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

        "*** YOUR CODE HERE ***"

        # print(successorGameState)
        s = 1
        ll = newFood.asList()
        foodCnt = float('inf')
        for food in ll:
            dist = manhattanDistance(food,newPos)
            foodCnt = min(s/(dist+1),foodCnt)
        
        Gcnt = float('inf')
        for ghost in successorGameState.getGhostPositions():
            dist = manhattanDistance(ghost ,newPos)
            Gcnt = min(-s/(dist+1),Gcnt)
        foodCnt *= 13
        Gcnt *= 10
        return successorGameState.getScore()+Gcnt+foodCnt


def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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
        
        
        def minimax(agent , depth ,gameState):
            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return self.evaluationFunction(gameState)
            if agent == 0:
                sc = float('-inf')
                for action in gameState.getLegalActions(agent):
                    sc = max(sc,minimax(1,depth,gameState.generateSuccessor(agent ,action)))
                return sc
            else:
                nextag = agent+1
                if(gameState.getNumAgents() == nextag):
                    nextag = 0
                    depth += 1
                sc = float('inf')
                for action in gameState.getLegalActions(agent):
                    sc = min(sc,minimax(nextag,depth,gameState.generateSuccessor(agent,action)))
                return sc

        actions = gameState.getLegalActions(0)
        mx_score,mx_score_idx = float('-inf'),None
        for idx in range(len(actions)):
            mini = minimax(1,0,gameState.generateSuccessor(0,actions[idx]))
            if(mx_score < mini):
                mx_score = mini
                mx_score_idx = idx
        return actions[mx_score_idx]
    
        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def minimaxa(agent , depth ,gameState ,alpha,beta):
            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return self.evaluationFunction(gameState)
            if agent == 0:
                bsc = float('-inf')
                for action in gameState.getLegalActions(agent):
                    sc = minimaxa(1,depth,gameState.generateSuccessor(agent ,action),alpha,beta)
                    bsc = max(bsc,sc)
                    alpha = max(alpha,sc)
                    if(beta <= alpha):
                        break
                return bsc
            else:
                nextag = agent+1
                if(gameState.getNumAgents() == nextag):
                    nextag = 0
                    depth += 1
                bsc = float('inf')
                for action in gameState.getLegalActions(agent):
                    sc = minimaxa(nextag,depth,gameState.generateSuccessor(agent,action),alpha,beta)
                    bsc = min(bsc,sc)
                    beta = min(beta,sc)
                    if(beta <= alpha):
                        break
                return bsc

        actions = gameState.getLegalActions(0)
        mx_score,mx_score_idx = float('-inf'),None
        alpha = float('-inf')
        beta = float('inf')
        for idx in range(len(actions)):
            mini = minimaxa(1,0,gameState.generateSuccessor(0,actions[idx]),alpha,beta)
            if(mx_score < mini):
                mx_score = mini
                mx_score_idx = idx
        return actions[mx_score_idx]


        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
       
        
        def expectimax(agent , depth ,gameState):
            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return self.evaluationFunction(gameState)
            if agent == 0:
                sc = float('-inf')
                for action in gameState.getLegalActions(agent):
                    sc = max(sc,expectimax(1,depth,gameState.generateSuccessor(agent ,action)))
                return sc
            else:
                nextag = agent+1
                if(gameState.getNumAgents() == nextag):
                    nextag = 0
                    depth += 1
                asc = 0
                for action in gameState.getLegalActions(agent):
                    asc += expectimax(nextag,depth,gameState.generateSuccessor(agent,action))
                return asc/(len(gameState.getLegalActions(agent)))
            

        actions = gameState.getLegalActions(0)
        mx_score,mx_score_idx = float('-inf'),None
        for idx in range(len(actions)):
            mini = expectimax(1,0,gameState.generateSuccessor(0,actions[idx]))
            if(mx_score < mini):
                mx_score = mini
                mx_score_idx = idx
        return actions[mx_score_idx]

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
