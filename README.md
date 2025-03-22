# Sudoku Solver using A* Algorithm

## Description

This project implements a Sudoku solver using the **A* search algorithm**. The solver efficiently finds the solution to a given Sudoku puzzle by evaluating the state space and using a heuristic to prioritize solving the most constrained cells first. The goal is to use the A* algorithm, which combines a cost function and a heuristic function, to solve Sudoku puzzles optimally.

The solver is designed to work with puzzles of varying difficulty levels, and it guarantees a solution that satisfies the following constraints:

- Every row must contain the digits 1-9 without repetition.
- Every column must contain the digits 1-9 without repetition.
- Each 3x3 sub-grid must contain the digits 1-9 without repetition.

## Features

- **A* Search Algorithm**: Uses A* to find the optimal solution by combining a cost function and a heuristic.
- **Heuristic Function**: The heuristic function evaluates the board based on how many conflicts (repeated digits) exist in rows, columns, and sub-grids.
- **Constrained Cell Selection**: Prioritizes cells with the fewest valid options to speed up the search.
- **Performance Metrics**: Tracks and displays the number of attempts, the size of the open queue, and heuristic values throughout the search process.


