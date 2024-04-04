# About this project
Repository submitted to fulfil the requirements of CS3821: Final Year Project Report.
Title: Single-agent and multi-agent search in maze games


# Getting started

## Prerequisites
To run this project, you need to install the following:
* Python 3.11.8 (recommended)
* Project dependencies specified in the requirements.txt file

## Installation (Windows)
`git clone https://github.com/TomRoscow/CS3821-fyp.git`
`python -m venv .venv`
`.venv\Scripts\activate.bat`
`pip install -r requirements.txt`

## How to run
The project specification details 9 deliverables. For clarity, each deliverable is demonstrated by running a dedicated script that calls the necessary algorithm and visualisation functions to demonstrate a working version of the code, including a pop-up window, to fulfil the deliverable requirements.

Recommended usage:
`python -m deliverable1`


# Repo structure
.
├── images/             # Images used for visualisation
├── output/             # Outputs produced by the scripts during execution
├── report/             # Report and other documents included in the submission
├── scripts/            # Scripts corresponding to each deliverable
├── src/                # Source code for algorithms, visualisation, and maze game
│   ├── graph_search/   # Single-agent and multi-agent graph search algorithms
├── test/               # Unit tests
├── README.txt
├── requirements.txt
└── <deliverables scripts>

## Scripts
The scripts are as follows:
| file name                  | description                                                           |
| -------------------------- | --------------------------------------------------------------------- |
| deliverable1.py            | Graphical visualisation of the maze game                              |
| deliverable2.py            | Depth-first and breadth-first search  for maze navigation             |
| deliverable3.py            | Uniform-cost graph search for maze navigation                         |
| deliverable4.py            | A* algorithm for efficient path-finding                               |
| deliverable5-comparison.py | Comparison of A* and greedy performance of single-agent path finding  |
| deliverable5.py            | A* and greedy search for single-agent path-finding                    |
| deliverable6.py            | Multi-agent search with a reflex agent                                |
| deliverable7.py            | Minimax algorithm for adversarial multi-agent search                  |