
import queue as q
import sys 
class State: 
    def __init__(self, missionariesLeft, cannibalsLeft, missionariesRight, cannibalsRight, boat, parent, action, cost): 
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
            newState = State(self.missionariesLeft - 2, self.cannibalsLeft, self.missionariesRight + 2, self.cannibalsRight, 'R', self, 'MM', self.cost + 1)
            if newState.isValidState():
                successors.append(newState)
            newState = State(self.missionariesLeft - 1, self.cannibalsLeft - 1, self.missionariesRight + 1, self.cannibalsRight + 1, 'R', self, 'MC', self.cost + 1)
            if newState.isValidState():
                successors.append(newState)
            newState = State(self.missionariesLeft, self.cannibalsLeft - 2, self.missionariesRight, self.cannibalsRight + 2, 'R', self, 'CC', self.cost + 1)
            if newState.isValidState():
                successors.append(newState)
            newState = State(self.missionariesLeft - 1,  self.cannibalsLeft, self.missionariesRight + 1, self.cannibalsRight, 'R', self, 'M', self.cost + 1)
            if newState.isValidState():
                successors.append(newState)
            newState = State(self.missionariesLeft, self.cannibalsLeft - 1, self.missionariesRight, self.cannibalsRight + 1, 'R', self, 'C', self.cost + 1)
            if newState.isValidState():
                successors.append(newState)
 
        else:
            newState = State(self.missionariesLeft + 2, self.cannibalsLeft, self.missionariesRight - 2, self.cannibalsRight, 'L', self, 'MM', self.cost + 1)
            if newState.isValidState():
                successors.append(newState)
            newState = State(self.missionariesLeft + 1, self.cannibalsLeft + 1, self.missionariesRight - 1, self.cannibalsRight - 1, 'L', self, 'MC', self.cost + 1)
            if newState.isValidState():
                successors.append(newState)
            newState = State(self.missionariesLeft, self.cannibalsLeft + 2, self.missionariesRight, self.cannibalsRight - 2, 'L', self, 'CC', self.cost + 1)
            if newState.isValidState():
                successors.append(newState)
            newState = State(self.missionariesLeft + 1, self.cannibalsLeft, self.missionariesRight - 1, self.cannibalsRight, 'L', self, 'M', self.cost + 1)
            if newState.isValidState():
                successors.append(newState)
            newState = State(self.missionariesLeft, self.cannibalsLeft + 1, self.missionariesRight, self.cannibalsRight - 1, 'L', self, 'C', self.cost + 1)
            if newState.isValidState():
                successors.append(newState)
        return successors

    #getters 
    
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

#for finding goal state
    def __eq__(self, other):
        return (self.missionariesLeft == other.missionariesLeft and 
                self.missionariesRight == other.missionariesRight and 
                self.cannibalsLeft == other.cannibalsLeft and 
                self.cannibalsRight == other.cannibalsRight and 
                self.boat == other.boat)
    def __hash__(self):
        return hash((self.missionariesLeft, self.cannibalsLeft, self.missionariesRight, self.cannibalsRight, self.boat))

class Problem: 

    def __init__(self, initialState, goalState):
        self.initialState = initialState;     
        self.goalState = goalState;
    

    def DFS(self, state):
        visited = set() 
        nodeCount = [0]
        
        return self.explore(state, visited, nodeCount)

    def explore(self, state, visited, nodeCount):
    # Check if current state is goal
        if state == self.goalState:
            return nodeCount[0], state
        
        visited.add(state)
        nodeCount[0] += 1
        
        for s in state.successor():
            if s not in visited:
                result = self.explore(s, visited, nodeCount)
                if result is not None:
                    return result  
        
        return None
        

    def BFS(self, state):
        visited = set() 
        nodeCount = [0]

        queue = q.Queue()
        queue.put(state)
        visited.add(state)
        while not queue.empty():
            current_state = queue.get()
            if current_state == self.goalState:
                return nodeCount[0], current_state
            for s in current_state.successor():
                if s not in visited:
                    visited.add(s)
                    nodeCount[0] += 1
                    queue.put(s)
                    
        return None
def readInput(fileName):
    lines = []
    with open(fileName, 'r') as file: 
        line = file.readline().strip().replace(" ", "").split(",")
        state = State(int(line[0].strip()), int(line[1].strip()), int(line[2].strip()), int(line[3].strip()), line[4].strip(), None, None, 0)
        
    return state;
def createSol(state):
    path = []
    cost = state.getCost()
    while state.getParent() is not None:
        path.append(state)
        state = state.getParent()
    path.reverse()
    return path, cost
def main(): 
#    input = sys.argv[1] # i included this for your convinience. you can just run python 3 solution_q2.py input.txt >> output.txt
    state = readInput("input.txt") #read inputs store in list of states
    problem = Problem(state, State(0, 0, state.getMissionariesLeft() + state.getMissionariesRight(), state.getCannibalsRight() + state.getCannibalsLeft() , 'R', None, None, 0)) # problem def
    dfsNodeCount, dfsGoalState= problem.DFS(state) # this needs to return the goal state as well
    bfsNodeCount, bfsGoalState = problem.BFS(state)
    if dfsGoalState is None:
        print("No solution found using DFS")
    else:
        dfsPath, dfsCost = createSol(dfsGoalState)
        path = []
        for step in dfsPath:
            path.append([step.getMissionariesLeft(), step.getCannibalsLeft(), step.getMissionariesRight(), step.getCannibalsRight(),step.getBoat(), step.getAction(), step.getCost()])
        print("The solution of Q1.1.a (DFS) is:")
        print("Solution Path: ", path)
        print("Total Cost: ", dfsCost) 
        print("Nodes Traversed: ", dfsNodeCount)
    if bfsGoalState is None: 
        print("No solution found for BFS")
    else: 
        bfsPath, bfsCost = createSol(bfsGoalState)
        path = []
        for step in bfsPath:
            path.append([step.getMissionariesLeft(), step.getCannibalsLeft(), step.getMissionariesRight(), step.getCannibalsRight(),step.getBoat(), step.getAction(), step.getCost()])
        print("The solution of Q1.1.b (BFS) is:")
        print("BFS Solution Path: ", path)
        print("Cost: ", bfsCost)
        print("Nodes Traversed: ", bfsNodeCount)
   

if __name__ == "__main__":
    main()
## fix input reading