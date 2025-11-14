import heapq as h
import sys
import math

class State: 
    def __init__(self, missionariesLeft, cannibalsLeft,  missionariesRight, cannibalsRight, boat, parent, action, cost): 
        self.missionariesLeft = missionariesLeft; 
        self.missionariesRight = missionariesRight; 
        self.cannibalsLeft = cannibalsLeft; 
        self.cannibalsRight = cannibalsRight; 
        self.boat = boat
        self.parent = parent; 
        self.action = action 
        self.cost = cost
    
    def isValidState(self):
        if self.missionariesLeft < 0 or self.missionariesRight < 0 or self.cannibalsLeft < 0 or self.cannibalsRight < 0:
            return False
        else:
            if self.missionariesLeft > 0 or self.missionariesRight > 0: 
                if self.missionariesLeft < self.cannibalsLeft and self.missionariesLeft != 0: 
                    return False
                if self.missionariesRight < self.cannibalsRight and self.missionariesRight != 0: 
                    return False
        return True
    
    def successor(self):
        successors = []
        #5 opts on each side. either 1 or 2 missionaries, 1 or 2 cannibals, or 1 of each. depends on where boat is
        if self.boat == 'L':
            newState = State(self.missionariesLeft - 2, self.cannibalsLeft, self.missionariesRight + 2, self.cannibalsRight, 'R', self, 'MM', self.cost + 4)
            if newState.isValidState():
                
                successors.append(newState)
            newState = State(self.missionariesLeft - 1, self.cannibalsLeft - 1,  self.missionariesRight + 1, self.cannibalsRight + 1, 'R', self, 'MC', self.cost + 3)
            if newState.isValidState():
                
                successors.append(newState)
            newState = State(self.missionariesLeft, self.cannibalsLeft - 2, self.missionariesRight, self.cannibalsRight + 2, 'R', self, 'CC', self.cost + 2)
            if newState.isValidState():
                
                successors.append(newState)
            newState = State(self.missionariesLeft - 1,  self.cannibalsLeft, self.missionariesRight + 1,self.cannibalsRight, 'R', self, 'M', self.cost + 2)
            if newState.isValidState():
                
                successors.append(newState)
            newState = State(self.missionariesLeft, self.cannibalsLeft - 1, self.missionariesRight, self.cannibalsRight + 1, 'R', self, 'C', self.cost + 1)
            if newState.isValidState():
                
                successors.append(newState)
        else:
            newState = State(self.missionariesLeft + 2, self.cannibalsLeft, self.missionariesRight - 2, self.cannibalsRight, 'L', self, 'MM', self.cost + 4)
            if newState.isValidState():
                
                successors.append(newState)
            newState = State(self.missionariesLeft + 1, self.cannibalsLeft + 1, self.missionariesRight - 1,self.cannibalsRight - 1, 'L', self, 'MC', self.cost + 3)
            if newState.isValidState():
                
                successors.append(newState)
            newState = State(self.missionariesLeft, self.cannibalsLeft + 2, self.missionariesRight, self.cannibalsRight - 2, 'L', self, 'CC', self.cost + 2)
            if newState.isValidState():
                
                successors.append(newState)
            newState = State(self.missionariesLeft + 1,  self.cannibalsLeft, self.missionariesRight - 1,self.cannibalsRight, 'L', self, 'M', self.cost + 2)
            if newState.isValidState():
                
                successors.append(newState)
            newState = State(self.missionariesLeft, self.cannibalsLeft + 1, self.missionariesRight, self.cannibalsRight - 1, 'L', self, 'C', self.cost + 1)
            if newState.isValidState():
                
                successors.append(newState)
        return successors

    def getHeruisticOne(self):
        return 2 * self.missionariesLeft + self.cannibalsLeft
    def getHeuristicTwo(self):
        val = math.ceil((2 * self.getMissionariesLeft() + self.getCannibalsLeft()) / 3)
        return val
    def getHeruisticThree(self):
        return (self.getMissionariesLeft()**2) + (self.getCannibalsLeft()**2)
    def copy(self):
        return State(self.missionariesLeft, self.missionariesRight, self.cannibalsLeft, self.cannibalsRight, self.boat, self.parent, self.action, self.cost)
    def ceiling(self,num):
        if num % 1 == 0:
            return int(num)
        else:
            return int(num) + 1
    def getMissionariesLeft(self):
        return self.missionariesLeft;
    def getMissionariesRight(self):
        return self.missionariesRight;
    def getCannibalsLeft(self):
        return self.cannibalsLeft;
    def getCannibalsRight(self):
        return self.cannibalsRight;
    def getBoat(self):
        return self.boat;
    def getAction(self):
        return self.action;
    def getCost(self):
        return self.cost;
    def getParent(self):
        return self.parent;
    def setCost(self, val):
        self.cost = val

     #for finding goal state
    def __eq__(self, other):
        return (self.missionariesLeft == other.missionariesLeft and 
                self.missionariesRight == other.missionariesRight and 
                self.cannibalsLeft == other.cannibalsLeft and 
                self.cannibalsRight == other.cannibalsRight and 
                self.boat == other.boat)
    #for in op
    def __hash__(self):
        return hash((self.missionariesLeft, self.missionariesRight, self.cannibalsLeft, self.cannibalsRight, self.boat))
    
    #for heap
    def __le__ (self, other):
        return self.cost <= other.cost
    def __gt__ (self, other):
        return self.cost > other.cost
class Problem: 
    def __init__(self, initialState, goalState): 
        self.initialState = initialState; 
        self.goalState = goalState; 

    def Astar(self, state, heursitic):
        visited = set()
        nodeCount = 0
        front = []
        h.heappush(front, (state.getCost(), state))
        while front != []:
            nodeCount += 1
            currentState = h.heappop(front)[1]
            if currentState == self.goalState:
                return nodeCount, currentState
            visited.add(currentState)
            for successor in currentState.successor():
                if successor not in visited:
                    if heursitic == 1:
                        h.heappush(front, (successor.getCost() + successor.getHeruisticOne(), successor))
                    elif heursitic == 2:
                        h.heappush(front, (successor.getCost() + successor.getHeuristicTwo(), successor))
                    else: 
                        h.heappush(front, (successor.getCost() + successor.getHeruisticThree(), successor))
                   ## h.heappush(front, (successor.getCost() + (successor.getHeruisticOne() if heursitic == 1 else successor.getHeuristicTwo()), successor))
        return nodeCount, None


def readInput(fileName):
    lines = []
    with open(fileName, 'r') as file: 
        lines = file.readlines()
        line = lines[0].strip().replace(" ", "").split(",")
        state = State(int(line[0].strip()), int(line[1].strip()), int(line[2].strip()), int(line[3].strip()), line[4].strip(), None, None, 0)
    return state;
def createSol(finalState):
    path =[]
    cost = finalState.getCost()
    path.append(finalState)
    while finalState is not None: 
        path.append(finalState)
        finalState = finalState.getParent()

    path.reverse()
    return cost, path;


        
def main():
##   input = sys.argv[1]
    state = readInput("input.txt")
    problem = Problem(state, State(0, 0, state.missionariesLeft + state.missionariesRight, state.cannibalsLeft + state.cannibalsRight, 'R', None, None, 0))
    astarNodeCount, astarGoalState = problem.Astar(state, heursitic=1)
    astartNodeCount2, astarGoalState2 = problem.Astar(state, heursitic=2)
    aStartNodeCount3, astarGoalState3 = problem.Astar(state, heursitic=3)

    if astarGoalState is None:
        print("No solution found using A* with Heuristic 1")
    else: 
        astarCost, astarPath = createSol(astarGoalState)
        path = []
        for step in astarPath:
            path.append([step.getMissionariesLeft(), step.getCannibalsLeft(), step.getMissionariesRight(), step.getCannibalsRight(),step.getBoat(), step.getAction(), step.getCost()])
        print("the solution of Q3.1 (Heuristic 1) is:")
        print("Solution path: ", path)
        print("Cost: ", astarCost)
        print("Number of node expansions: ", astarNodeCount)
    if astarGoalState2 is None:
        print("No solution found using A* with Heuristic 2")
    else:
        aStartCost2, astarPath2 = createSol(astarGoalState2)
        path = []

        for step in astarPath2:
            path.append([step.getMissionariesLeft(), step.getCannibalsLeft(), step.getMissionariesRight(), step.getCannibalsRight(),step.getBoat(), step.getAction(), step.getCost()])

        print("The solution of Q3.1 (Heuristic 2) is:")
        print("Solution Path: ", path)
        print("Cost: ", aStartCost2)
        print("Nodes Traverse: ", astartNodeCount2)
    if astarGoalState3 is None:
        print("No solution found using A* with Heuristic 3")
    else:
        aStartCost3, astarPath3 = createSol(astarGoalState3)
        path = []
        for step in astarPath3:
            path.append([step.getMissionariesLeft(), step.getCannibalsLeft(), step.getMissionariesRight(), step.getCannibalsRight(),step.getBoat(), step.getAction(), step.getCost()])
        print("The solution of Q3.1 (Heuristic 3) is:")
        print("Solution Path: ", path)
        print("Cost: ", aStartCost3)
        print("Nodes Traverse: ", aStartNodeCount3)
if __name__ == "__main__": 
    main()