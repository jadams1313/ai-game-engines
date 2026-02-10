"""
Search result data structures.

This module provides classes for encapsulating the results of search algorithms,
including solution paths, statistics, and metadata.
"""

from dataclasses import dataclass
from typing import List, Optional, Any
from .state import State


@dataclass
class SearchResult:
    """
    Container for search algorithm results.
    
    Attributes:
        success: Whether a solution was found
        goal_state: The goal state reached (if found)
        path: Sequence of states from initial to goal
        actions: Sequence of actions taken
        cost: Total path cost
        nodes_expanded: Number of nodes expanded during search
        nodes_generated: Total number of nodes generated
        max_frontier_size: Maximum size of the frontier during search
        time_elapsed: Time taken in seconds (optional)
        algorithm: Name of the algorithm used
        metadata: Additional algorithm-specific information
    """
    success: bool
    goal_state: Optional[State] = None
    path: List[State] = None
    actions: List[Any] = None
    cost: float = float('inf')
    nodes_expanded: int = 0
    nodes_generated: int = 0
    max_frontier_size: int = 0
    time_elapsed: float = 0.0
    algorithm: str = ""
    metadata: dict = None
    
    def __post_init__(self):
        """Initialize empty lists and dicts if None."""
        if self.path is None:
            self.path = []
        if self.actions is None:
            self.actions = []
        if self.metadata is None:
            self.metadata = {}
    
    @property
    def path_length(self) -> int:
        """Get the number of states in the solution path."""
        return len(self.path)
    
    @property
    def solution_depth(self) -> int:
        """Get the solution depth (number of actions)."""
        return len(self.actions)
    
    def __repr__(self) -> str:
        """Formatted string representation of the result."""
        if not self.success:
            return (f"SearchResult(success=False, "
                   f"nodes_expanded={self.nodes_expanded}, "
                   f"algorithm={self.algorithm})")
        
        return (f"SearchResult(success=True, "
               f"cost={self.cost:.2f}, "
               f"depth={self.solution_depth}, "
               f"nodes_expanded={self.nodes_expanded}, "
               f"algorithm={self.algorithm})")
    
    def summary(self) -> str:
        """
        Get a human-readable summary of the search result.
        
        Returns:
            Multi-line string summarizing the search
        """
        lines = [
            f"{'='*60}",
            f"Search Result - {self.algorithm}",
            f"{'='*60}",
        ]
        
        if self.success:
            lines.extend([
                f"✓ Solution found!",
                f"  Cost: {self.cost:.2f}",
                f"  Path length: {self.path_length} states",
                f"  Solution depth: {self.solution_depth} actions",
            ])
        else:
            lines.append(f"✗ No solution found")
        
        lines.extend([
            f"",
            f"Search Statistics:",
            f"  Nodes expanded: {self.nodes_expanded}",
            f"  Nodes generated: {self.nodes_generated}",
            f"  Max frontier size: {self.max_frontier_size}",
        ])
        
        if self.time_elapsed > 0:
            lines.append(f"  Time elapsed: {self.time_elapsed:.4f} seconds")
        
        if self.metadata:
            lines.append(f"")
            lines.append(f"Additional Information:")
            for key, value in self.metadata.items():
                lines.append(f"  {key}: {value}")
        
        lines.append(f"{'='*60}")
        
        return "\n".join(lines)
    
    def print_path(self) -> None:
        """Print the solution path in a readable format."""
        if not self.success or not self.path:
            print("No solution path available")
            return
        
        print(f"\nSolution Path ({len(self.path)} states):")
        print(f"{'='*60}")
        
        for i, state in enumerate(self.path):
            if i == 0:
                print(f"Initial: {state}")
            elif i == len(self.path) - 1:
                print(f"Goal:    {state}")
            else:
                action = self.actions[i-1] if i-1 < len(self.actions) else "?"
                print(f"Step {i}: {state} (action: {action})")