"""
Informed search algorithms.

This module implements search strategies that use domain-specific knowledge
(heuristics) to guide the search:
- Uniform Cost Search (UCS)
- A* Search
- Greedy Best-First Search
"""

import heapq
from typing import Set, Dict, Optional
import time

from ...core import State, Problem, HeuristicProblem, SearchResult


def uniform_cost_search(problem: Problem) -> SearchResult:
    """
    Uniform Cost Search algorithm.
    
    Expands the node with the lowest path cost first.
    Uses a priority queue ordered by cumulative cost (g-score).
    Optimal and complete for non-negative edge costs.
    
    Args:
        problem: The search problem to solve
        
    Returns:
        SearchResult containing the solution (if found) and statistics
    """
    start_time = time.time()
    initial_state = problem.initial_state
    
    # Priority queue: (cost, counter, state)
    # Counter ensures FIFO ordering for states with equal cost
    counter = 0
    frontier = [(initial_state.cost, counter, initial_state)]
    counter += 1
    
    # Track best cost to reach each state
    visited: Dict[State, float] = {}
    
    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 1
    
    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        
        # Get state with lowest cost
        current_cost, _, current_state = heapq.heappop(frontier)
        
        # Skip if we've found a better path to this state
        if current_state in visited and visited[current_state] < current_cost:
            continue
        
        visited[current_state] = current_cost
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
                algorithm="Uniform Cost Search (UCS)"
            )
        
        # Expand successors
        successors = problem.get_successors(current_state)
        for successor in successors:
            # Only add if we haven't seen it or found a better path
            if successor not in visited or successor.cost < visited[successor]:
                heapq.heappush(frontier, (successor.cost, counter, successor))
                counter += 1
                nodes_generated += 1
    
    # No solution found
    return SearchResult(
        success=False,
        nodes_expanded=nodes_expanded,
        nodes_generated=nodes_generated,
        max_frontier_size=max_frontier_size,
        time_elapsed=time.time() - start_time,
        algorithm="Uniform Cost Search (UCS)"
    )


def a_star_search(problem: HeuristicProblem) -> SearchResult:
    """
    A* Search algorithm.
    
    Uses both path cost (g) and heuristic estimate (h) to guide search.
    Expands nodes with lowest f-score = g + h.
    Optimal if heuristic is admissible; optimally efficient if consistent.
    
    Args:
        problem: The heuristic search problem to solve
        
    Returns:
        SearchResult containing the solution (if found) and statistics
    """
    start_time = time.time()
    initial_state = problem.initial_state
    
    # Priority queue: (f_score, counter, state)
    counter = 0
    initial_h = problem.heuristic(initial_state)
    initial_f = initial_state.cost + initial_h
    frontier = [(initial_f, counter, initial_state)]
    counter += 1
    
    # Track best cost to reach each state
    visited: Dict[State, float] = {}
    
    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 1
    
    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        
        # Get state with lowest f-score
        current_f, _, current_state = heapq.heappop(frontier)
        
        # Skip if we've found a better path
        if current_state in visited and visited[current_state] < current_state.cost:
            continue
        
        visited[current_state] = current_state.cost
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
                algorithm="A* Search"
            )
        
        # Expand successors
        successors = problem.get_successors(current_state)
        for successor in successors:
            # Only add if we haven't seen it or found a better path
            if successor not in visited or successor.cost < visited[successor]:
                h_score = problem.heuristic(successor)
                f_score = successor.cost + h_score
                heapq.heappush(frontier, (f_score, counter, successor))
                counter += 1
                nodes_generated += 1
    
    # No solution found
    return SearchResult(
        success=False,
        nodes_expanded=nodes_expanded,
        nodes_generated=nodes_generated,
        max_frontier_size=max_frontier_size,
        time_elapsed=time.time() - start_time,
        algorithm="A* Search"
    )


def greedy_best_first_search(problem: HeuristicProblem) -> SearchResult:
    """
    Greedy Best-First Search algorithm.
    
    Expands the node that appears to be closest to the goal based on heuristic.
    Uses only h-score (not g) to order the frontier.
    Not optimal, but often faster than A*.
    
    Args:
        problem: The heuristic search problem to solve
        
    Returns:
        SearchResult containing the solution (if found) and statistics
    """
    start_time = time.time()
    initial_state = problem.initial_state
    
    # Priority queue: (h_score, counter, state)
    counter = 0
    initial_h = problem.heuristic(initial_state)
    frontier = [(initial_h, counter, initial_state)]
    counter += 1
    
    visited: Set[State] = set()
    
    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 1
    
    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        
        # Get state with lowest heuristic value
        _, _, current_state = heapq.heappop(frontier)
        
        # Skip if already visited
        if current_state in visited:
            continue
        
        visited.add(current_state)
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
                algorithm="Greedy Best-First Search"
            )
        
        # Expand successors
        successors = problem.get_successors(current_state)
        for successor in successors:
            if successor not in visited:
                h_score = problem.heuristic(successor)
                heapq.heappush(frontier, (h_score, counter, successor))
                counter += 1
                nodes_generated += 1
    
    # No solution found
    return SearchResult(
        success=False,
        nodes_expanded=nodes_expanded,
        nodes_generated=nodes_generated,
        max_frontier_size=max_frontier_size,
        time_elapsed=time.time() - start_time,
        algorithm="Greedy Best-First Search"
    )