"""
Uninformed (blind) search algorithms.

This module implements classic uninformed search strategies that don't use
domain-specific knowledge:
- Depth-First Search (DFS)
- Breadth-First Search (BFS)
- Depth-Limited Search (DLS)
- Iterative Deepening Search (IDS)
"""

from collections import deque
from typing import Optional, Set
import time

from ...core import State, Problem, SearchResult


def depth_first_search(problem: Problem, max_depth: Optional[int] = None) -> SearchResult:
    """
    Depth-First Search algorithm.
    
    Explores as far as possible along each branch before backtracking.
    Uses a stack (LIFO) for the frontier. Not optimal, not complete (without depth limit).
    
    Args:
        problem: The search problem to solve
        max_depth: Maximum depth to explore (None for unlimited)
        
    Returns:
        SearchResult containing the solution (if found) and statistics
    """
    start_time = time.time()
    initial_state = problem.initial_state
    
    # Stack for DFS (we'll use recursion with explicit visited set)
    visited: Set[State] = set()
    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 0
    
    def dfs_recursive(state: State, depth: int) -> Optional[State]:
        """Recursive DFS implementation."""
        nonlocal nodes_expanded, nodes_generated, max_frontier_size
        
        # Check depth limit
        if max_depth is not None and depth > max_depth:
            return None
        
        # Check if goal
        if problem.is_goal(state):
            return state
        
        # Mark as visited
        visited.add(state)
        nodes_expanded += 1
        
        # Explore successors
        successors = problem.get_successors(state)
        nodes_generated += len(successors)
        
        for successor in successors:
            if successor not in visited:
                result = dfs_recursive(successor, depth + 1)
                if result is not None:
                    return result
        
        return None
    
    # Run DFS
    goal_state = dfs_recursive(initial_state, 0)
    
    # Build result
    success = goal_state is not None
    path = goal_state.get_path() if goal_state else []
    actions = goal_state.get_actions() if goal_state else []
    cost = goal_state.cost if goal_state else float('inf')
    
    return SearchResult(
        success=success,
        goal_state=goal_state,
        path=path,
        actions=actions,
        cost=cost,
        nodes_expanded=nodes_expanded,
        nodes_generated=nodes_generated,
        max_frontier_size=len(visited),
        time_elapsed=time.time() - start_time,
        algorithm="Depth-First Search (DFS)"
    )


def breadth_first_search(problem: Problem) -> SearchResult:
    """
    Breadth-First Search algorithm.
    
    Explores all neighbors at present depth before moving to nodes at next depth.
    Uses a queue (FIFO) for the frontier. Complete and optimal for unit costs.
    
    Args:
        problem: The search problem to solve
        
    Returns:
        SearchResult containing the solution (if found) and statistics
    """
    start_time = time.time()
    initial_state = problem.initial_state
    
    # Queue for BFS
    frontier = deque([initial_state])
    visited: Set[State] = {initial_state}
    
    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 1
    
    while frontier:
        # Track frontier size
        max_frontier_size = max(max_frontier_size, len(frontier))
        
        # Get next state from frontier
        current_state = frontier.popleft()
        nodes_expanded += 1
        
        # Check if goal
        if problem.is_goal(current_state):
            path = current_state.get_path()
            actions = current_state.get_actions()
            
            return SearchResult(
                success=True,
                goal_state=current_state,
                path=path,
                actions=actions,
                cost=current_state.cost,
                nodes_expanded=nodes_expanded,
                nodes_generated=nodes_generated,
                max_frontier_size=max_frontier_size,
                time_elapsed=time.time() - start_time,
                algorithm="Breadth-First Search (BFS)"
            )
        
        # Expand successors
        successors = problem.get_successors(current_state)
        for successor in successors:
            if successor not in visited:
                visited.add(successor)
                frontier.append(successor)
                nodes_generated += 1
    
    # No solution found
    return SearchResult(
        success=False,
        nodes_expanded=nodes_expanded,
        nodes_generated=nodes_generated,
        max_frontier_size=max_frontier_size,
        time_elapsed=time.time() - start_time,
        algorithm="Breadth-First Search (BFS)"
    )


def depth_limited_search(problem: Problem, limit: int) -> SearchResult:
    """
    Depth-Limited Search algorithm.
    
    DFS with a depth limit to avoid infinite loops in infinite state spaces.
    
    Args:
        problem: The search problem to solve
        limit: Maximum depth to search
        
    Returns:
        SearchResult containing the solution (if found) and statistics
    """
    result = depth_first_search(problem, max_depth=limit)
    result.algorithm = f"Depth-Limited Search (DLS, limit={limit})"
    result.metadata['depth_limit'] = limit
    return result


def iterative_deepening_search(problem: Problem, max_limit: int = 100) -> SearchResult:
    """
    Iterative Deepening Search algorithm.
    
    Repeatedly applies depth-limited search with increasing depth limits.
    Combines the space efficiency of DFS with the completeness of BFS.
    
    Args:
        problem: The search problem to solve
        max_limit: Maximum depth limit to try
        
    Returns:
        SearchResult containing the solution (if found) and statistics
    """
    start_time = time.time()
    total_nodes_expanded = 0
    total_nodes_generated = 0
    
    for depth_limit in range(max_limit + 1):
        result = depth_limited_search(problem, depth_limit)
        
        total_nodes_expanded += result.nodes_expanded
        total_nodes_generated += result.nodes_generated
        
        if result.success:
            result.algorithm = f"Iterative Deepening Search (IDS, depth={depth_limit})"
            result.nodes_expanded = total_nodes_expanded
            result.nodes_generated = total_nodes_generated
            result.time_elapsed = time.time() - start_time
            result.metadata['final_depth_limit'] = depth_limit
            return result
    
    # No solution found within max_limit
    return SearchResult(
        success=False,
        nodes_expanded=total_nodes_expanded,
        nodes_generated=total_nodes_generated,
        time_elapsed=time.time() - start_time,
        algorithm=f"Iterative Deepening Search (IDS, max_limit={max_limit})",
        metadata={'max_depth_limit': max_limit}
    )