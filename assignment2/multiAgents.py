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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        """
          return the actions with the best score.
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

        """
          return a socre
        """
        # Useful information you can extract from a GameState (pacman.py)
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)    #new state after action
        newPos = successorGameState.getPacmanPosition()  # new position(x,y)
        newFood = successorGameState.getFood()           #remaining food
        newGhostStates = successorGameState.getGhostStates()

        "*** YOUR CODE HERE ***"
        remain_food=newFood.asList()
        food_dis=[]
        Fmin=0
        score=successorGameState.getScore()

        for food in remain_food:
            dis=util.manhattanDistance(newPos,food)
            food_dis.append(dis)

        if len(food_dis)!=0: 
            Fmin=min(food_dis)                # find the nearest food distance
        
        if Fmin!=0:                           # food score desgin
            if Fmin<=2:
                score+=10/Fmin
            else:
                score+=5/Fmin

        Fghost=0
        ghostdis=[]
        ghostNum=0
        for ghost in newGhostStates:
            gdis=util.manhattanDistance(newPos,ghost.getPosition())       
            ghostdis.append(gdis)
            ghostNum+=1

        if len(ghostdis)!=0: 
            Fghost=min(ghostdis)              # find the nearest ghost distance

        if ghostNum!=0:
            ghostAverage=sum(ghostdis)/ghostNum    # average ghost distance
        else:
            ghostAverage=0

        danger=0
        if ghostAverage!=0 and Fghost!=0:
            danger=4/Fghost+4/ghostAverage        
        
        if danger==4 or danger==8:               # high danger suituation!  Fghost=1 or 2    
            score-=20*danger                # in this suituation, pacman should run instead of eating food
        elif danger>2:                           # middle danger suituaion
            score-=10*danger
        else:                                    # low danger, pacman should try to eat food
            score-=0

        return score   
        
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
        """
        actions=gameState.getLegalActions(0)
        l=[]
        v=-1e10
        action=Directions.STOP

        for a in actions:
            state=gameState.generateSuccessor(0,a)
            score=self.getMin(state,0,1)          # all possible actions for pacman
            l.append((score,a))
        
        # choose the best one, return the action
        for a,b in l:
            if a>v:
                v=a
                action=b    
        return action     
        """
        return self.minimax(gameState,self.depth,0)           

    def minimax(self,gameState,depth,agentIndex):
        actions=gameState.getLegalActions(0)
        l=[]
        v=-1e10
        action=Directions.STOP

        for a in actions:
            state=gameState.generateSuccessor(0,a)
            score=self.getMin(state,0,1)          # all possible actions for pacman
            l.append((score,a))
        
        # choose the best one, return the action
        for a,b in l:
            if a>v:
                v=a
                action=b    
        return action    
    
    # actions by ghosts   (ghost >1)    index>=1
    def getMin(self,gameState,depth,agentIndex):
        value=1e10
        num=gameState.getNumAgents()
        
        if depth==self.depth or gameState.isWin() or gameState.isLose():        # stop criterion
            return self.evaluationFunction(gameState)
          
        for action in gameState.getLegalActions(agentIndex):
            state=gameState.generateSuccessor(agentIndex,action) 
            if agentIndex==num-1:           # the last ghost, go into the next depth(pacman)
                value=min(value,self.getMax(state,depth+1,agentIndex=0))
            else:                              # the next ghost: agentIndex+1
                value=min(value,self.getMin(state,depth,agentIndex+1))
            
        return value
            
    # pacman actions        pacman: index==0
    def getMax(self,gameState,depth,agentIndex=0):  
        value=-1e10

        if depth==self.depth or gameState.isWin() or gameState.isLose():        # stop criterion
            return self.evaluationFunction(gameState)

        for action in gameState.getLegalActions(0):
            state=gameState.generateSuccessor(0,action) 
            value=max(value,self.getMin(state,depth,1))

        return value
    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        a=-1e10
        b=1e10
        return self.getAlpha(gameState,0,0,a,b)[1]
    
    def getAlpha(self,gameState,depth,agentIndex,alpha=1e10,beta=-1e10):
        value=-1e10
        finalAction=Directions.STOP
        if depth==self.depth or gameState.isWin() or gameState.isLose():        
            return self.evaluationFunction(gameState),None
        
        legalActions=gameState.getLegalActions(agentIndex)
        actionList=list(enumerate(legalActions))
        for index,action in actionList:
            state=gameState.generateSuccessor(agentIndex,action)
            score=self.getBeta(state,depth,agentIndex+1,alpha,beta)[0]

            if score>value:
                value=score
                finalAction=action
            
            if value>beta:
                return value,action
            
            alpha=max(alpha,value)
            
        return value,finalAction               # return max value and its action
    
    def getBeta(self,gameState,depth,agentIndex,alpha=1e10,beta=-1e10):
        value=1e10
        num=gameState.getNumAgents()
        finalAction=Directions.STOP

        if depth==self.depth or gameState.isWin() or gameState.isLose():        
            return self.evaluationFunction(gameState),None
        
        for action in gameState.getLegalActions(agentIndex):
            state=gameState.generateSuccessor(agentIndex,action)
            if agentIndex==num-1:
                score=self.getAlpha(state,depth+1,0,alpha,beta)[0]
            else:
                score=self.getBeta(state,depth,agentIndex+1,alpha,beta)[0]

            if value>score:
                value=score
                finalAction=action

            if value<alpha:
                return value,action
            
            beta=min(beta,value)

        return value,finalAction

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
        value=-1e10
        finalAction=Directions.STOP
        legalActions=gameState.getLegalActions(0)
        l=[]

        for action in legalActions:
            state=gameState.generateSuccessor(0,action)
            score=self.expection(state,0,1)
            l.append((score,action))
        
        for a,b in l:
            if a>value:
                value=a
                finalAction=b    
        return finalAction 

    # the same as minimax
    def getMax(self,gameState,depth,agentIndex):
        legalActions=gameState.getLegalActions(agentIndex)
        if depth==self.depth or gameState.isWin() or gameState.isLose():        
            return self.evaluationFunction(gameState)
        value=-1e10
        for action in legalActions:
            # from the first ghost
            state=gameState.generateSuccessor(agentIndex,action)
            score=self.expection(state,depth,1)
            value=max(value,score)
        return value

    def expection(self,gameState,depth,agentIndex):
        legalActions=gameState.getLegalActions(agentIndex)
        num=gameState.getNumAgents()
        number=0.0

        if depth==self.depth or gameState.isWin() or gameState.isLose():        
            return self.evaluationFunction(gameState)
        
        for action in legalActions:
            state=gameState.generateSuccessor(agentIndex,action)
            # the last ghost
            if agentIndex==num-1:
                number+=self.getMax(state,depth+1,0)
            else:
                number+=self.expection(state,depth,agentIndex+1)
        
        return float(number/(len(legalActions)))

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()  # new position(x,y)
    newFood = currentGameState.getFood()           #remaining food
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    remain_food=newFood.asList()
    food_dis=[]
    Fmin=0
    score=currentGameState.getScore()
        
    for food in remain_food:
        dis=util.manhattanDistance(newPos,food)
        food_dis.append(dis)

    if len(food_dis)!=0: 
        Fmin=min(food_dis)                # find the nearest food distance
        
    if Fmin!=0:                           # food score desgin
        if Fmin<=2:
            score+=10/Fmin
        else:
            score+=5/Fmin
    
    # remaining food number. the less the number is, the better 
    foodNum=len(remain_food)
    score-=5*foodNum
    
    # in scare time, the ghosts are not harmful.  So this should be an extra score.
    # scare time should be longer (better)
    score+=2*sum(newScaredTimes)

    Fghost=0
    ghostdis=[]
    ghostNum=0
    for ghost in newGhostStates:
        gdis=util.manhattanDistance(newPos,ghost.getPosition())       
        ghostdis.append(gdis)
        ghostNum+=1

    if len(ghostdis)!=0: 
        Fghost=min(ghostdis)              # find the nearest ghost distance

    if ghostNum!=0:
        ghostAverage=sum(ghostdis)/ghostNum    # average ghost distance
    else:
        ghostAverage=0

    danger=0
    if ghostAverage!=0 and Fghost!=0:
        danger=4/Fghost+4/ghostAverage        
        
    if danger==4 or danger==8:               # high danger suituation!  Fghost=1 or 2    
        score-=20*danger                # in this suituation, pacman should run instead of eating food
    elif danger>2:                           # middle danger suituaion
        score-=10*danger

    return score  

# Abbreviation
better = betterEvaluationFunction

