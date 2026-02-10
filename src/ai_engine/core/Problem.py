"""
Abstract Problem definition for search algorithms.

This module provides the Problem class that encapsulates a search problem,
including initial state, goal specification, and problem-specific logic.
"""

from abc import ABC, abstractmethod
from typing import Optional
from .state import State


class Problem(ABC):
    """
    Abstract base class for search problems.
    
    A problem consists of:
    - An initial state
    - A goal specification
    - Actions and transition model (via State.get_successors)
    - Path cost (via State.cost)
    """
    
    def __init__(self, initial_state: State, goal_state: Optional[State] = None):
        """
        Initialize a search problem.
        
        Args:
            initial_state: The starting state
            goal_state: The goal state (if goal is a specific state)
        """
        self._initial_state = initial_state
        self._goal_state = goal_state
    
    @property
    def initial_state(self) -> State:
        """Get the initial state of the problem."""
        return self._initial_state
    
    @property
    def goal_state(self) -> Optional[State]:
        """Get the goal state (if applicable)."""
        return self._goal_state
    
    @abstractmethod
    def is_goal(self, state: State) -> bool:
        """
        Check if a state satisfies the goal condition.
        
        This allows for flexible goal specification:
        - Specific state (state == self.goal_state)
        - Goal test (e.g., all items in certain positions)
        - Multiple possible goals
        
        Args:
            state: The state to check
            
        Returns:
            True if state is a goal state, False otherwise
        """
        pass
    
    def get_successors(self, state: State) -> list[State]:
        """
        Get all valid successor states from a given state.
        
        This is a convenience method that delegates to State.get_successors().
        Override if you need problem-specific filtering.
        
        Args:
            state: The current state
            
        Returns:
            List of valid successor states
        """
        return state.get_successors()
    
    def get_cost(self, state: State, action: any, next_state: State) -> float:
        """
        Get the cost of taking an action from state to next_state.
        
        Default implementation returns the difference in cumulative costs.
        Override for custom cost functions.
        
        Args:
            state: The current state
            action: The action taken
            next_state: The resulting state
            
        Returns:
            Cost of the transition
        """
        return next_state.cost - state.cost
    
    def __repr__(self) -> str:
        """String representation of the problem."""
        return f"{self.__class__.__name__}(initial={self._initial_state})"


class HeuristicProblem(Problem):
    """
    Extension of Problem for informed search algorithms.
    
    This adds heuristic evaluation capability for algorithms like A*.
    """
    
    @abstractmethod
    def heuristic(self, state: State) -> float:
        """
        Estimate the cost from state to the nearest goal.
        
        The heuristic should be:
        - Admissible: Never overestimate the actual cost
        - Consistent: h(n) <= cost(n, n') + h(n') for all n, n'
        
        Args:
            state: The state to evaluate
            
        Returns:
            Estimated cost to reach a goal state
        """
        pass