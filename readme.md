# Ford-Fulkerson Algorithm for Maximum Flow with BFS

This project implements the Ford-Fulkerson algorithm using Breadth-First Search (BFS) to calculate the maximum flow in a directed graph. The graph is constructed from a dataset of flight networks stored in a CSV file. This README outlines the project's purpose, usage, and setup instructions.

## Features

- **Graph Construction**: Automatically builds a directed graph from a CSV dataset using NetworkX.
- **Ford-Fulkerson Algorithm**: Implements the classic algorithm for computing maximum flow with augmenting paths found via BFS.
- **Path Tracking**: Stores all augmenting paths and their corresponding flow values.
- **CSV Integration**: Reads input datasets and exports results with computed flow values.
- **Data Preprocessing**: Cleans and merges raw datasets to generate the input for the algorithm.

## Requirements

- **Python**: 3.7+
- **Required Libraries**:
  - `pandas`
  - `networkx`

Install dependencies using pip:

>```bash
>pip install pandas networkx
>``` 