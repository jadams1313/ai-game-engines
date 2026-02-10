"""
Setup script for AI Algorithms Toolkit
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-game-engines",
    version="0.1.0",
    author="jadams",
    author_email="adamsjay1313@gmail.com",
    description="A comprehensive toolkit of AI algorithms including search, adversarial games, RL, and probabilistic reasoning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-algorithms-toolkit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
        "viz": [
            "matplotlib>=3.5.0",
            "seaborn>=0.11.0",
        ],
        "all": [
            "gymnasium>=0.27.0",  # For RL environments
            "pygame>=2.1.0",      # For game GUIs
            "pandas>=1.3.0",      # For data handling
            "scikit-learn>=1.0.0", # For ML utilities
        ]
    },
    entry_points={
        "console_scripts": [
            "ai-toolkit-demo=examples.demo_search:main",
        ],
    },
)