"""
Abstract State representation for search problems.

This module provides the base State class that all problem-specific states
should inherit from. States are immutable representations of problem configurations.
"""

from abc import ABC, abstractmethod
from typing import List, Any, Tuple


class State(ABC):
    """
    Abstract base class for states in search problems.
    
    A state represents a configuration of the problem world. States must be
    hashable and comparable to enable efficient storage and duplicate detection.
    """
    
    def __init__(self, parent: 'State' = None, action: Any = None, cost: float = 0):
        """
        Initialize a state.
        
        Args:
            parent: The parent state that generated this state
            action: The action taken to reach this state from parent
            cost: The cumulative cost from the initial state (g-score)
        """
        self._parent = parent
        self._action = action
        self._cost = cost
    
    @abstractmethod
    def is_valid(self) -> bool:
        """
        Check if this state is valid according to problem constraints.
        
        Returns:
            True if the state is valid, False otherwise
        """
        pass
    
    @abstractmethod
    def get_successors(self) -> List['State']:
        """
        Generate all valid successor states from this state.
        
        Returns:
            List of valid successor states
        """
        pass
    
    @abstractmethod
    def __eq__(self, other: 'State') -> bool:
        """
        Check equality with another state.
        
        States are equal if they represent the same problem configuration,
        regardless of how they were reached.
        
        Args:
            other: Another state to compare with
            
        Returns:
            True if states are equivalent, False otherwise
        """
        pass
    
    @abstractmethod
    def __hash__(self) -> int:
        """
        Generate hash for this state.
        
        States with the same configuration must have the same hash.
        This enables efficient storage in sets and dictionaries.
        
        Returns:
            Hash value for this state
        """
        pass
    
    @abstractmethod
    def __repr__(self) -> str:
        """
        String representation of the state for debugging.
        
        Returns:
            Human-readable string describing the state
        """
        pass
    
    def __lt__(self, other: 'State') -> bool:
        """
        Compare states for priority queue ordering (by cost).
        
        Args:
            other: Another state to compare with
            
        Returns:
            True if this state has lower cost than other
        """
        return self._cost < other._cost
    
    def __le__(self, other: 'State') -> bool:
        """Less than or equal comparison."""
        return self._cost <= other._cost
    
    def __gt__(self, other: 'State') -> bool:
        """Greater than comparison."""
        return self._cost > other._cost
    
    # Properties for accessing state metadata
    
    @property
    def parent(self) -> 'State':
        """Get the parent state."""
        return self._parent
    
    @property
    def action(self) -> Any:
        """Get the action that led to this state."""
        return self._action
    
    @property
    def cost(self) -> float:
        """Get the cumulative cost to reach this state (g-score)."""
        return self._cost
    
    def get_path(self) -> List['State']:
        """
        Reconstruct the path from the initial state to this state.
        
        Returns:
            List of states from initial state to this state
        """
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        path.reverse()
        return path
    
    def get_actions(self) -> List[Any]:
        """
        Get the sequence of actions from the initial state to this state.
        
        Returns:
            List of actions taken from initial state to this state
        """
        actions = []
        current = self
        while current.parent is not None:
            actions.append(current.action)
            current = current.parent
        actions.reverse()
        return actions


class StateWithHeuristic(State):
    """
    Extension of State that supports heuristic evaluation for informed search.
    
    This is used by algorithms like A* and Greedy Best-First Search.
    """
    
    @abstractmethod
    def heuristic(self, goal: State) -> float:
        """
        Estimate the cost from this state to the goal.
        
        The heuristic should be admissible (never overestimate) for A* optimality.
        
        Args:
            goal: The goal state
            
        Returns:
            Estimated cost to reach the goal (h-score)
        """
        pass
    
    @property
    def f_score(self) -> float:
        """
        Get the f-score (g + h) for A* search.
        
        Note: This requires a goal state to be set. Typically used during search.
        
        Returns:
            Sum of cost and heuristic estimate
        """
        # This is a simplified version. In practice, you'd pass goal to heuristic
        # or store it during search. We'll handle this in the search algorithms.
        return self._cost