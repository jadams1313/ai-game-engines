# 📁 Complete File Structure


```
ai-game-engines
│
├── README.md                     ← Project overview & quick start
├── RESTRUCTURING_PLAN.md         ← Architecture & design decisions
├── NEXT_STEPS.md                 ← Roadmap for growth
├── PROJECT_STRUCTURE.md          ← Project strutcture file
│
├──  setup.py                      ← Package installation config
├──  demo_search.py                ← Working demonstration
│
└──  ai_toolkit/                   ← Main package
    ├── __init__.py
    │
    ├──  adverse agents/            ← Untouched, but has gui for demo
    │   ├── tictactoe-ai    
    │        └── tictactoe-ai-master/
    │            ...
    │   └── minimax_agent.py
    ├──  probablistic/              ← Uses probabilistic graph models to predict diabetes and the famous burgalary problem
    │   ├── Naive Bayes-Classification-Data.csv
    │   ├── project.zip
    │   ├── diabetes_classifer.py
    │   └── burglary_problem.py
    ├──  rl/                        ← Uses OpenAI's gymnasium to create reinforcement learning agents in black jack and the frozen lake env. 
    │   ├── black_jack_agent.py
    │   ├── frozen_lake_agent.py
    │   ├── project.zip
    │   ├── test_black_jack_agent.py
    │   └── test_frozen_lake_agent.py
    ├──  core/                     ← Abstract base classes
    │   ├── __init__.py
    │   ├── state.py                 ← State abstraction
    │   ├── problem.py               ← Problem abstraction
    │   └── search_result.py         ← Result container
    │
    └──  search/                   ← Search algorithms & problems
        ├── __init__.py
        │
        ├── algorithms/              ← Algorithm implementations
        │   ├── __init__.py
        │   ├── uninformed.py        ← DFS, BFS, DLS, IDS
        │   └── informed.py          ← UCS, A*, Greedy Best-First
        │
        └── problems/                ← Problem implementations
            ├── __init__.py
            └── missionaries_cannibals.py  ← Fully refactored!
```

