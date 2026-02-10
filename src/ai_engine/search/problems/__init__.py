"""
Classic search problems.

Implementations of well-known search problems for testing and demonstration.
"""

from .missionaries_cannibals import (
    MissionariesCannibalsState,
    MissionariesCannibalsProblem,
    MissionariesCannibalsHeuristicProblem,
    load_from_file
)

__all__ = [
    'MissionariesCannibalsState',
    'MissionariesCannibalsProblem',
    'MissionariesCannibalsHeuristicProblem',
    'load_from_file',
]