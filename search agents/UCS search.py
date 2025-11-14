import heapq as h
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

    def successor(self, cost_model):
        successors = []
        #5 opts on each side. either 1 or 2 missionaries, 1 or 2 cannibals, or 1 of each. depends on where boat is
        if(cost_model == "Cost Model A"):
            if self.boat == 'L':
                newState = State(self.missionariesLeft - 2, self.cannibalsLeft, self.missionariesRight + 2, self.cannibalsRight, 'R', self, 'MM', self.cost + 4)
                if newState.isValidState():
                    successors.append(newState)
                newState = State(self.missionariesLeft - 1, self.cannibalsLeft - 1, self.missionariesRight + 1, self.cannibalsRight + 1, 'R', self, 'MC', self.cost + 3)
                if newState.isValidState():
                    successors.append(newState)
                newState = State(self.missionariesLeft, self.cannibalsLeft - 2, self.missionariesRight, self.cannibalsRight + 2, 'R', self, 'CC', self.cost + 2)
                if newState.isValidState():
                    successors.append(newState)
                newState = State(self.missionariesLeft - 1,  self.cannibalsLeft, self.missionariesRight + 1, self.cannibalsRight, 'R', self, 'M', self.cost + 2)
                if newState.isValidState():
                    successors.append(newState)
                newState = State(self.missionariesLeft, self.cannibalsLeft - 1, self.missionariesRight, self.cannibalsRight + 1, 'R', self, 'C', self.cost + 1)
                if newState.isValidState():
                    successors.append(newState)
    
            else:
                newState = State(self.missionariesLeft + 2, self.cannibalsLeft, self.missionariesRight - 2, self.cannibalsRight, 'L', self, 'MM', self.cost + 4)
                if newState.isValidState():
                    successors.append(newState)
                newState = State(self.missionariesLeft + 1, self.cannibalsLeft + 1, self.missionariesRight - 1, self.cannibalsRight - 1, 'L', self, 'MC', self.cost + 3)
                if newState.isValidState():
                    successors.append(newState)
                newState = State(self.missionariesLeft, self.cannibalsLeft + 2, self.missionariesRight, self.cannibalsRight - 2, 'L', self, 'CC', self.cost + 2)
                if newState.isValidState():
                    successors.append(newState)
                newState = State(self.missionariesLeft + 1, self.cannibalsLeft, self.missionariesRight - 1, self.cannibalsRight, 'L', self, 'M', self.cost + 2)
                if newState.isValidState():
                    successors.append(newState)
                newState = State(self.missionariesLeft, self.cannibalsLeft + 1, self.missionariesRight, self.cannibalsRight - 1, 'L', self, 'C', self.cost + 1)
                if newState.isValidState():
                    successors.append(newState)
        else: #cost model b
            if self.boat == 'L':
                newState = State(self.missionariesLeft - 2, self.cannibalsLeft, self.missionariesRight + 2, self.cannibalsRight, 'R', self, 'MM', self.cost + 2)
                if newState.isValidState():
                    successors.append(newState)
                newState = State(self.missionariesLeft - 1, self.cannibalsLeft - 1, self.missionariesRight + 1, self.cannibalsRight + 1, 'R', self, 'MC', self.cost + 2)
                if newState.isValidState():
                    successors.append(newState)
                newState = State(self.missionariesLeft, self.cannibalsLeft - 2, self.missionariesRight, self.cannibalsRight + 2, 'R', self, 'CC', self.cost + 2)
                if newState.isValidState():
                    successors.append(newState)
                newState = State(self.missionariesLeft - 1,  self.cannibalsLeft, self.missionariesRight + 1, self.cannibalsRight, 'R', self, 'M', self.cost + 2)
                if newState.isValidState():
                    successors.append(newState)
                newState = State(self.missionariesLeft, self.cannibalsLeft - 1, self.missionariesRight, self.cannibalsRight + 1, 'R', self, 'C', self.cost + 2)
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
    def __le__ (self, other):
        return self.cost <= other.cost
    def __gt__ (self, other):
        return self.cost > other.cost
    def __hash__(self):
        return hash((self.missionariesLeft, self.missionariesRight, self.cannibalsLeft, self.cannibalsRight, self.boat))
class Problem: 
    def __init__(self, initialState, goalState): 
        self.initialState = initialState; 
        self.goalState = goalState;
    def UCS(self, state, cost_model):
        visited = set()
        nodeCount = 0
        front = []
        h.heappush(front, (state.getCost(), state))

        while front != []:
            nodeCount += 1
            currentState = h.heappop(front)[1] #heapq pops on first el of a tuple
            visited.add(currentState)
            if currentState == self.goalState:
                return nodeCount, currentState
            
            for successor in currentState.successor(cost_model):
                if successor not in visited:
                    h.heappush(front, (successor.getCost(), successor))

        return nodeCount, None
def readInput(fileName):
    lines = []
    with open(fileName, 'r') as file: 
        lines = file.readlines()
        line = lines[0].strip().replace(" ", "").split(",")

        if len(lines) < 2:
            cost_model = None
        else:
            cost_model = lines[1].strip()
        
        state = State(int(line[0].strip()), int(line[1].strip()), int(line[2].strip()), int(line[3].strip()), line[4].strip(), None, None, 0)
    
    return state, cost_model;
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
    #read cost model and inputs
#    input = sys.argv[1]
    state, cost_model = readInput("input.txt")
    problem = Problem(state, State(0, 0, state.getMissionariesLeft() + state.getMissionariesRight(), state.getCannibalsLeft() + state.getCannibalsRight(), 'R', None, None, 0))
    if cost_model is None:
        ucsNodeCount, ucsGoalState = problem.UCS(state, "Cost Model A")
        ucsNodeCount2, ucsGoalState2 = problem.UCS(state, "Cost Model B")
        ucsCost, ucsPath = createSol(ucsGoalState)
        ucsCost2, ucsPath2 = createSol(ucsGoalState2)
        path = []
        path2 = []
        for step in ucsPath:
            path.append([step.getMissionariesLeft(), step.getCannibalsLeft(), step.getMissionariesRight(), step.getCannibalsRight(),step.getBoat(), step.getAction(), step.getCost()])
        for step in ucsPath2:
            path2.append([step.getMissionariesLeft(), step.getCannibalsLeft(), step.getMissionariesRight(), step.getCannibalsRight(),step.getBoat(), step.getAction(), step.getCost()])
        print("The solution to question 2.1 UCS is (Cost Model A):")
        print("UCS Solution Path: ", path)
        print("Cost: ", ucsCost)
        print("Nodes Traverse: ", ucsNodeCount)
        print("\n")
        print("The solution to question 2.1 UCS is (Cost Model B):")
        print("UCS Solution Path: ", path2)
        print("Cost: ", ucsCost2)
        print("Nodes Traverse: ", ucsNodeCount2)

    else:
        if cost_model == "Cost Model A":
            ucsNodeCount, ucsGoalState = problem.UCS(state, "Cost Model A")
        else:
            ucsNodeCount, ucsGoalState = problem.UCS(state, "Cost Model B")

        ucsCost, ucsPath = createSol(ucsGoalState)
        path = []
        for step in ucsPath:
            path.append([step.getMissionariesLeft(), step.getCannibalsLeft(), step.getMissionariesRight(), step.getCannibalsRight(),step.getBoat(), step.getAction(), step.getCost()])
        print(f"The solution to question 2.1 UCS is ({cost_model}):")
        print("UCS Solution Path: ", path)
        print("Cost: ", ucsCost)
        print("Nodes Traverse: ", ucsNodeCount)



    

if __name__ == "__main__":
    main()