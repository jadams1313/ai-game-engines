"""
AI Algorithms Toolkit

A comprehensive collection of AI algorithms including search, adversarial games,
reinforcement learning, and probabilistic reasoning.

Modules:
    core: Abstract base classes and interfaces
    search: Search algorithms and problems
"""

__version__ = '0.1.0'
__author__ = 'jadams'

from . import core
from . import search

__all__ = ['core', 'search']


