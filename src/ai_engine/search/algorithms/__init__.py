"""
Search algorithms module.

Provides implementations of both uninformed and informed search strategies.
"""

from .uninformed import (
    depth_first_search,
    breadth_first_search,
    depth_limited_search,
    iterative_deepening_search
)

from .informed import (
    uniform_cost_search,
    a_star_search,
    greedy_best_first_search
)

__all__ = [
    # Uninformed
    'depth_first_search',
    'breadth_first_search',
    'depth_limited_search',
    'iterative_deepening_search',
    # Informed
    'uniform_cost_search',
    'a_star_search',
    'greedy_best_first_search',
]