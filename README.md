# AI Algorithms Toolkit

A clean, extensible Python toolkit implementing classic AI algorithms with a focus on modularity and educational clarity.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This toolkit provides professional implementations of fundamental AI algorithms across multiple domains:

- **Search Algorithms**: DFS, BFS, UCS, A*, Greedy Best-First
- **Adversarial Search**: Minimax, Alpha-Beta Pruning (coming soon)
- **Reinforcement Learning**: Q-Learning, Value Iteration (coming soon)
- **Probabilistic Reasoning**: Bayesian Networks, Naive Bayes (coming soon)

## Key Features

✨ **Clean Architecture**: Abstract base classes enable easy extension  
🔌 **Modular Design**: Use components independently or together  
📊 **Rich Results**: Comprehensive statistics and metadata  
🧪 **Well-Tested**: Extensive test coverage (coming soon)  
📚 **Educational**: Clear code with detailed docstrings  
🚀 **Production-Ready**: Type hints, error handling, and logging  

## Installation

### From Source

```bash
git clone https://github.com/yourusername/ai-algorithms-toolkit.git
cd ai-algorithms-toolkit
pip install -e .
```

### With Development Dependencies

```bash
pip install -e ".[dev]"
```

## Quick Start

### Basic Search Example

```python
from ai_toolkit.search.algorithms import breadth_first_search
from ai_toolkit.search.problems import MissionariesCannibalsProblem

# Create a problem
problem = MissionariesCannibalsProblem(missionaries=3, cannibals=3)

# Solve it
result = breadth_first_search(problem)

# Display results
print(result.summary())

# Access solution details
if result.success:
    print(f"Solution found with cost: {result.cost}")
    print(f"Path length: {len(result.path)}")
    print(f"Actions: {result.actions}")
```

### Comparing Algorithms

```python
from ai_toolkit.search.algorithms import (
    depth_first_search,
    breadth_first_search,
    uniform_cost_search,
    a_star_search
)
from ai_toolkit.search.problems import MissionariesCannibalsHeuristicProblem

problem = MissionariesCannibalsHeuristicProblem(
    missionaries=3, 
    cannibals=3,
    heuristic_type='simple'
)

algorithms = {
    'DFS': depth_first_search,
    'BFS': breadth_first_search,
    'UCS': uniform_cost_search,
    'A*': a_star_search
}

for name, algorithm in algorithms.items():
    result = algorithm(problem)
    print(f"{name}: {result.nodes_expanded} nodes, cost={result.cost}")
```

## Architecture

### Core Abstractions

#### State
Abstract base class for problem states:
```python
class State(ABC):
    @abstractmethod
    def is_valid(self) -> bool:
        """Check if state is valid"""
        
    @abstractmethod
    def get_successors(self) -> List['State']:
        """Generate successor states"""
        
    @abstractmethod
    def __eq__(self, other) -> bool:
        """Check equality"""
        
    @abstractmethod
    def __hash__(self) -> int:
        """Enable storage in sets/dicts"""
```

#### Problem
Defines a search problem:
```python
class Problem(ABC):
    @property
    def initial_state(self) -> State:
        """Starting state"""
        
    @abstractmethod
    def is_goal(self, state: State) -> bool:
        """Check if state is goal"""
```

#### SearchResult
Comprehensive result container:
```python
@dataclass
class SearchResult:
    success: bool
    goal_state: Optional[State]
    path: List[State]
    actions: List[Any]
    cost: float
    nodes_expanded: int
    nodes_generated: int
    max_frontier_size: int
    time_elapsed: float
    algorithm: str
    metadata: dict
```

## Project Structure

```
ai_toolkit/
├── core/
│   ├── state.py           # Abstract State class
│   ├── problem.py         # Abstract Problem class
│   └── search_result.py   # SearchResult container
├── search/
│   ├── algorithms/
│   │   ├── uninformed.py  # DFS, BFS, IDS
│   │   └── informed.py    # UCS, A*, Greedy
│   └── problems/
│       └── missionaries_cannibals.py
└── utils/
    └── ...
```

## Extending the Toolkit

### Creating a New Problem

1. **Define your state class**:
```python
from ai_toolkit.core import State

class MyState(State):
    def __init__(self, data, parent=None, action=None, cost=0):
        super().__init__(parent, action, cost)
        self.data = data
    
    def is_valid(self) -> bool:
        # Your validation logic
        return True
    
    def get_successors(self) -> List['MyState']:
        # Generate successor states
        successors = []
        # ... your logic ...
        return successors
    
    def __eq__(self, other):
        return self.data == other.data
    
    def __hash__(self):
        return hash(self.data)
```

2. **Define your problem class**:
```python
from ai_toolkit.core import Problem

class MyProblem(Problem):
    def __init__(self, initial_data, goal_data):
        initial = MyState(initial_data)
        goal = MyState(goal_data)
        super().__init__(initial, goal)
    
    def is_goal(self, state: MyState) -> bool:
        return state == self.goal_state
```

3. **Solve it**:
```python
from ai_toolkit.search.algorithms import a_star_search

problem = MyProblem(initial_data, goal_data)
result = a_star_search(problem)
```

### Adding a New Algorithm

```python
from ai_toolkit.core import Problem, SearchResult
import time

def my_custom_search(problem: Problem) -> SearchResult:
    """My custom search algorithm."""
    start_time = time.time()
    
    # Your algorithm implementation
    # ...
    
    return SearchResult(
        success=True/False,
        goal_state=found_goal,
        path=solution_path,
        # ... other fields ...
        algorithm="My Custom Search"
    )
```

## Running Examples

### Demo Script
```bash
python demo_search.py
```

This runs comprehensive demonstrations of:
- Algorithm comparisons
- Cost model variations
- Heuristic comparisons

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black ai_toolkit/
```

### Type Checking
```bash
mypy ai_toolkit/
```

## Benchmarking

Compare algorithm performance:
```python
from ai_toolkit.search.problems import MissionariesCannibalsProblem
from ai_toolkit.search.algorithms import *

problem = MissionariesCannibalsProblem(3, 3)

results = {
    'DFS': depth_first_search(problem),
    'BFS': breadth_first_search(problem),
    'UCS': uniform_cost_search(problem),
}

for name, result in results.items():
    print(f"{name}:")
    print(f"  Nodes expanded: {result.nodes_expanded}")
    print(f"  Time: {result.time_elapsed:.4f}s")
```

## Roadmap

- [x] Core abstractions (State, Problem, SearchResult)
- [x] Uninformed search (DFS, BFS, IDS)
- [x] Informed search (UCS, A*, Greedy)
- [x] Missionaries and Cannibals problem
- [ ] More classic problems (8-puzzle, N-queens, etc.)
- [ ] Adversarial search module (Minimax, MCTS)
- [ ] Reinforcement learning module
- [ ] Probabilistic reasoning module
- [ ] Visualization utilities
- [ ] Web interface for demos
- [ ] Comprehensive test suite
- [ ] Performance benchmarks
- [ ] Documentation site

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

Implementations based on classic algorithms from:
- Russell & Norvig's "Artificial Intelligence: A Modern Approach"
- Cormen et al's "Introduction to Algorithms"

## Citation

If you use this toolkit in your research or teaching, please cite:
```bibtex
@software{ai_algorithms_toolkit,
  author = {Your Name},
  title = {AI Algorithms Toolkit},
  year = {2026},
  url = {https://github.com/yourusername/ai-algorithms-toolkit}
}
```

## Contact

- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

**Happy Algorithm Exploring! 🚀**