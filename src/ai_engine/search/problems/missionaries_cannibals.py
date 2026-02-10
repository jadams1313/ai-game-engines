"""
Missionaries and Cannibals Problem.

Classic river-crossing puzzle: Transport missionaries and cannibals across a river
such that missionaries are never outnumbered by cannibals on either side.

Problem Setup:
- N missionaries and N cannibals on the left bank
- One boat that can hold up to 2 people
- Goal: Get everyone to the right bank
- Constraint: Missionaries can never be outnumbered by cannibals on either bank
"""

from typing import List, Tuple, Optional
from ...core import State, Problem, HeuristicProblem


class MissionariesCannibalsState(State):
    """
    State representation for the Missionaries and Cannibals problem.
    
    Attributes:
        missionaries_left: Number of missionaries on left bank
        cannibals_left: Number of cannibals on left bank
        boat_location: 'L' for left bank, 'R' for right bank
        total_missionaries: Total number of missionaries
        total_cannibals: Total number of cannibals
    """
    
    # Possible actions: (missionaries, cannibals) to move
    ACTIONS = [
        ('MM', 2, 0),  # Two missionaries
        ('MC', 1, 1),  # One missionary, one cannibal
        ('CC', 0, 2),  # Two cannibals
        ('M', 1, 0),   # One missionary
        ('C', 0, 1),   # One cannibal
    ]
    
    def __init__(
        self,
        missionaries_left: int,
        cannibals_left: int,
        boat_location: str,
        total_missionaries: int,
        total_cannibals: int,
        parent: Optional['MissionariesCannibalsState'] = None,
        action: Optional[str] = None,
        cost: float = 0,
        cost_model: str = 'uniform'
    ):
        """
        Initialize a state.
        
        Args:
            missionaries_left: Number of missionaries on left bank
            cannibals_left: Number of cannibals on left bank
            boat_location: 'L' or 'R' indicating boat position
            total_missionaries: Total number of missionaries in problem
            total_cannibals: Total number of cannibals in problem
            parent: Parent state
            action: Action taken to reach this state
            cost: Cumulative cost
            cost_model: 'uniform', 'model_a', or 'model_b'
        """
        super().__init__(parent, action, cost)
        self.missionaries_left = missionaries_left
        self.cannibals_left = cannibals_left
        self.boat_location = boat_location
        self.total_missionaries = total_missionaries
        self.total_cannibals = total_cannibals
        self.cost_model = cost_model
    
    @property
    def missionaries_right(self) -> int:
        """Number of missionaries on right bank."""
        return self.total_missionaries - self.missionaries_left
    
    @property
    def cannibals_right(self) -> int:
        """Number of cannibals on right bank."""
        return self.total_cannibals - self.cannibals_left
    
    def is_valid(self) -> bool:
        """
        Check if state is valid.
        
        Valid if:
        1. No negative counts
        2. Missionaries never outnumbered by cannibals on either bank
           (unless there are 0 missionaries on that bank)
        """
        # Check for negative counts
        if (self.missionaries_left < 0 or self.cannibals_left < 0 or
            self.missionaries_right < 0 or self.cannibals_right < 0):
            return False
        
        # Check left bank: if there are missionaries, they must not be outnumbered
        if self.missionaries_left > 0:
            if self.missionaries_left < self.cannibals_left:
                return False
        
        # Check right bank: if there are missionaries, they must not be outnumbered
        if self.missionaries_right > 0:
            if self.missionaries_right < self.cannibals_right:
                return False
        
        return True
    
    def get_action_cost(self, action_name: str, m_count: int, c_count: int) -> float:
        """
        Calculate cost for an action based on the cost model.
        
        Args:
            action_name: Name of the action ('MM', 'MC', etc.)
            m_count: Number of missionaries moved
            c_count: Number of cannibals moved
            
        Returns:
            Cost of the action
        """
        if self.cost_model == 'uniform':
            return 1.0
        elif self.cost_model == 'model_a':
            # Cost Model A: Based on number and type of people
            # MM=4, MC=3, CC=2, M=2, C=1
            if action_name == 'MM':
                return 4.0
            elif action_name == 'MC':
                return 3.0
            elif action_name == 'CC':
                return 2.0
            elif action_name == 'M':
                return 2.0
            elif action_name == 'C':
                return 1.0
        elif self.cost_model == 'model_b':
            # Cost Model B: Left to right is cheaper than right to left
            # Left to right: 2, Right to left: 1
            if self.boat_location == 'L':  # Moving from left to right
                return 2.0
            else:  # Moving from right to left
                return 1.0
        
        return 1.0  # Default
    
    def get_successors(self) -> List['MissionariesCannibalsState']:
        """
        Generate all valid successor states.
        
        Returns:
            List of valid successor states
        """
        successors = []
        
        for action_name, m_to_move, c_to_move in self.ACTIONS:
            if self.boat_location == 'L':
                # Moving from left to right
                new_m_left = self.missionaries_left - m_to_move
                new_c_left = self.cannibals_left - c_to_move
                new_boat = 'R'
            else:
                # Moving from right to left
                new_m_left = self.missionaries_left + m_to_move
                new_c_left = self.cannibals_left + c_to_move
                new_boat = 'L'
            
            # Calculate cost for this action
            action_cost = self.get_action_cost(action_name, m_to_move, c_to_move)
            new_cost = self.cost + action_cost
            
            # Create new state
            new_state = MissionariesCannibalsState(
                new_m_left,
                new_c_left,
                new_boat,
                self.total_missionaries,
                self.total_cannibals,
                parent=self,
                action=action_name,
                cost=new_cost,
                cost_model=self.cost_model
            )
            
            # Only add if valid
            if new_state.is_valid():
                successors.append(new_state)
        
        return successors
    
    def __eq__(self, other: 'MissionariesCannibalsState') -> bool:
        """States are equal if they have the same configuration."""
        if not isinstance(other, MissionariesCannibalsState):
            return False
        return (self.missionaries_left == other.missionaries_left and
                self.cannibals_left == other.cannibals_left and
                self.boat_location == other.boat_location)
    
    def __hash__(self) -> int:
        """Hash based on state configuration."""
        return hash((self.missionaries_left, self.cannibals_left, self.boat_location))
    
    def __repr__(self) -> str:
        """String representation of the state."""
        return (f"[M:{self.missionaries_left} C:{self.cannibals_left} | "
                f"Boat:{'←' if self.boat_location == 'L' else '→'} | "
                f"M:{self.missionaries_right} C:{self.cannibals_right}]")


class MissionariesCannibalsProblem(Problem):
    """
    The Missionaries and Cannibals problem.
    
    Goal: Transport all missionaries and cannibals from left bank to right bank.
    """
    
    def __init__(
        self,
        missionaries: int = 3,
        cannibals: int = 3,
        cost_model: str = 'uniform'
    ):
        """
        Initialize the problem.
        
        Args:
            missionaries: Number of missionaries (default 3)
            cannibals: Number of cannibals (default 3)
            cost_model: Cost model to use ('uniform', 'model_a', 'model_b')
        """
        initial_state = MissionariesCannibalsState(
            missionaries_left=missionaries,
            cannibals_left=cannibals,
            boat_location='L',
            total_missionaries=missionaries,
            total_cannibals=cannibals,
            cost_model=cost_model
        )
        
        goal_state = MissionariesCannibalsState(
            missionaries_left=0,
            cannibals_left=0,
            boat_location='R',
            total_missionaries=missionaries,
            total_cannibals=cannibals,
            cost_model=cost_model
        )
        
        super().__init__(initial_state, goal_state)
        self.cost_model = cost_model
    
    def is_goal(self, state: MissionariesCannibalsState) -> bool:
        """Check if state is the goal state."""
        return state == self.goal_state


class MissionariesCannibalsHeuristicProblem(HeuristicProblem):
    """
    Heuristic version of Missionaries and Cannibals problem for A* search.
    """
    
    def __init__(
        self,
        missionaries: int = 3,
        cannibals: int = 3,
        cost_model: str = 'uniform',
        heuristic_type: str = 'simple'
    ):
        """
        Initialize the heuristic problem.
        
        Args:
            missionaries: Number of missionaries
            cannibals: Number of cannibals
            cost_model: Cost model to use
            heuristic_type: Type of heuristic ('simple', 'advanced', 'quadratic')
        """
        initial_state = MissionariesCannibalsState(
            missionaries_left=missionaries,
            cannibals_left=cannibals,
            boat_location='L',
            total_missionaries=missionaries,
            total_cannibals=cannibals,
            cost_model=cost_model
        )
        
        goal_state = MissionariesCannibalsState(
            missionaries_left=0,
            cannibals_left=0,
            boat_location='R',
            total_missionaries=missionaries,
            total_cannibals=cannibals,
            cost_model=cost_model
        )
        
        super().__init__(initial_state, goal_state)
        self.cost_model = cost_model
        self.heuristic_type = heuristic_type
    
    def is_goal(self, state: MissionariesCannibalsState) -> bool:
        """Check if state is the goal state."""
        return state == self.goal_state
    
    def heuristic(self, state: MissionariesCannibalsState) -> float:
        """
        Estimate cost from state to goal.
        
        Three heuristic options:
        1. 'simple': 2 * missionaries_left + cannibals_left
        2. 'advanced': ceil((2 * missionaries_left + cannibals_left) / 3)
        3. 'quadratic': missionaries_left^2 + cannibals_left^2
        """
        if self.heuristic_type == 'simple':
            # Heuristic 1: Weighted sum
            return 2.0 * state.missionaries_left + state.cannibals_left
        
        elif self.heuristic_type == 'advanced':
            # Heuristic 2: Estimate minimum trips needed
            people_left = 2 * state.missionaries_left + state.cannibals_left
            import math
            return math.ceil(people_left / 3.0)
        
        elif self.heuristic_type == 'quadratic':
            # Heuristic 3: Quadratic distance
            return float(state.missionaries_left ** 2 + state.cannibals_left ** 2)
        
        return 0.0


# Utility functions for loading from file

def load_from_file(filename: str) -> Tuple[MissionariesCannibalsProblem, Optional[str]]:
    """
    Load problem configuration from file.
    
    Expected format:
    Line 1: m_left, c_left, m_right, c_right, boat_location
    Line 2 (optional): cost_model
    
    Args:
        filename: Path to input file
        
    Returns:
        Tuple of (problem, cost_model)
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Parse first line
    line = lines[0].strip().replace(" ", "").split(",")
    m_left = int(line[0])
    c_left = int(line[1])
    # m_right and c_right are in the file but we calculate from totals
    # boat_location is in line[4]
    
    # Parse cost model if present
    cost_model = 'uniform'
    if len(lines) >= 2:
        cost_model_line = lines[1].strip()
        if 'Model A' in cost_model_line:
            cost_model = 'model_a'
        elif 'Model B' in cost_model_line:
            cost_model = 'model_b'
    
    # Create problem (assumes we start with everyone on left)
    total_m = m_left
    total_c = c_left
    
    problem = MissionariesCannibalsProblem(total_m, total_c, cost_model)
    
    return problem, cost_model