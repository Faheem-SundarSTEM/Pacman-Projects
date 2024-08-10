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

from genericpath import exists
from re import S
from typing import Tuple
import util
from collections import defaultdict 
import heapq

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

    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print( "Start's successors:", problem.getSuccessors(problem.getStartState()))

    # iterative slow 

    '''from util import Stack
    start = problem.getStartState()
    stack = Stack()
    stack.push((start,[]))
    visited = set()
    visited.add(start)

    while not stack.isEmpty():
        cur,path = stack.pop()
        if(problem.isGoalState(cur)):
            return path
        l = problem.getSuccessors(cur)
        for nei in l:
            if(nei[0] not in visited):
                visited.add(nei[0])
                npath = path+[nei[1]]
                stack.push((nei[0],npath))
    return []'''

    # recursive fast

    ans = []
    def dfs(u):
        nonlocal path,ans 
        visited.add(u[0])
        path.append(u[1])
        if(problem.isGoalState(u[0])):
            path.pop(0)
            ans = path.copy()
            # return path
        l = problem.getSuccessors(u[0])
        for v in l:
            if(v[0] not in visited):
                dfs((v[0],v[1]))
        if(len(path)>=1):path.pop()

    start = problem.getStartState()
    # stack = Stack()
    # stack.push((start,[]))
    visited = set()
    path = []
    dfs((start,'West'))

    return ans

    util.raiseNotDefined()

    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    from util import Queue
    start = problem.getStartState()

    queue = Queue()
    queue.push((start,[]))
    visited = []
    visited.append(start)

    while not queue.isEmpty():
        cur,path = queue.pop()
        if(problem.isGoalState(cur)):
            return path

        for nei in problem.getSuccessors(cur):
            if(nei[0] not in visited):
                visited.append(nei[0])
                queue.push((nei[0],path+[nei[1]]))

    return []

    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    print( "Start's successors:", problem.getSuccessors(problem.getStartState()))

    start = problem.getStartState()

    heap = []
    dist = defaultdict(lambda:float('inf'))
    parent = defaultdict(tuple)
    parent[start] = (None,None)
    dist[start] = 0
    heapq.heappush(heap,(0,start))
    path = []
    endnode = None
    while(heap):
        dis,cur = heapq.heappop(heap)
        print(cur)
        if(problem.isGoalState(cur)):
            endnode = cur

        for neib in problem.getSuccessors(cur):
            nei,dirt, gcost = neib
            if(dist[nei] > dis+gcost):
                dist[nei] = dis + gcost
                heapq.heappush(heap,(dist[nei] , nei))
                parent[nei] = (cur,dirt)
    
    s = endnode
    while(s != start):
        print(parent[s])
        path.append(parent[s][1])
        s = parent[s][0]


    path.reverse()
    return path

    util.raiseNotDefined()
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    start_ = problem.getStartState()
    start = tuple(start_)
    openlist = PriorityQueue()
    g_cost = defaultdict(lambda:-1) 
    g_cost[start] = 0
    f_cost = defaultdict(int)
    f_cost[start] = heuristic(start,problem)
    openlist.push(start,f_cost[start])
    parent = defaultdict(tuple)
    endnode = None
    while openlist:
        cur  = openlist.pop()
        if(problem.isGoalState(cur)):
            endnode = cur
            break
        l = problem.getSuccessors(cur)
        for nei in l:
            gon = g_cost[cur] + nei[2]
            if(g_cost[nei[0]]==-1 or gon < g_cost[nei[0]]):
                g_cost[nei[0]] = gon
                parent[nei[0]] = (cur,nei[1])
                f_cost[nei[0]] = gon + heuristic(nei[0],problem)
                openlist.push(nei[0],f_cost[nei[0]])

    s = endnode
    path = []
    while(s != start):
        path.append(parent[s][1])
        s = parent[s][0]


    path.reverse()
    return path



    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch