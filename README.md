
# **Unruly Solver: CSP and Simulated Annealing**

This repository contains a Python implementation of a solver for the **Unruly** puzzle, a binary logic game. The solver employs two approaches to find a solution:

1. **Constraint Satisfaction Problem (CSP) Formulation**: Solves the problem by applying constraints for valid Unruly boards.
2. **Simulated Annealing**: Uses a metaheuristic optimization algorithm to minimize rule violations iteratively.

Both approaches are designed to solve puzzles efficiently while providing metrics about their performance.

---

## **The Unruly Problem**

Unruly is a binary logic puzzle played on an \( n 	imes m \) grid, with the following constraints:
- Each row and column must contain an equal number of `1`s (black) and `0`s (white).
- No row or column may contain three or more consecutive cells of the same value.
- Predefined cells are fixed and cannot be altered.

The objective is to fill the board while satisfying all constraints.
You can play by yourself and see the input and output formatting of the table at [Unruly](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/unruly.html).

---

## **Solver Approaches**

### **1. CSP Formulation**
The CSP-based approach treats Unruly as a constraint satisfaction problem:
- **Variables**: Each cell in the grid.
- **Domains**: `{0, 1}` for each cell.
- **Constraints**:
  - Equal numbers of `0`s and `1`s in each row/column.
  - No three consecutive `0`s or `1`s in any row/column.
  - Fixed cells cannot change.

### **2. Simulated Annealing**
Simulated annealing minimizes the violations of constraints by iteratively exploring new states:
- Starts with a randomly filled board.
- Evaluates a state using an **objective function** that calculates the total violations.
- Applies a **temperature schedule** to probabilistically accept worse solutions early in the process, allowing exploration of the solution space.

The temperature decreases exponentially as the algorithm progresses, ensuring convergence to a near-optimal solution.

---

## **Features**

- **Input Parsing**:
  - The solver reads puzzles from a custom-encoded input file.
  - Predefined cells are decoded and stored as fixed positions.
- **Output Encoding**:
  - Solutions are written to a file with the same custom encoding for easy integration.
- **Customizable Parameters**:
  - Maximum steps for the simulated annealing algorithm can be specified.
- **Performance Metrics**:
  - Average success rate, violations, steps, and execution time are calculated over multiple runs.

---

## **Performance Metrics**

For a given puzzle and increasing maximum steps, the following metrics are recorded:
- **Success Rate**: Percentage of runs finding a valid solution.
- **Average Violations**: Mean number of rule violations in the final state.
- **Average Steps**: Mean number of steps taken before termination.
- **Execution Time**: Mean time taken to solve the puzzle.

---

## **How to Use**

### **1. Requirements**
- Python 3.x
- No additional dependencies (uses Python's standard library).

### **2. Input File Format**
The input file should be formatted as follows:
- **Grid Dimensions**: `n x m` (even numbers only).
- **Encoded Predefined Cells**: Each predefined cell is encoded as a sequence of characters representing its position.

Example:
```
6x6:aAaBacAdAeAfA
```

### **3. Running the Solver**
To execute the solver:

1. Provide the required inputs:
   - Input file name.
   - Maximum steps or max nodes expanded for simulated annealing or CSP respectively.

### **4. Output**
- The initial and final board configurations are printed to the console.
- The best solution found is saved to an output file in the appropriate encoding format.

---



## **Example Run**

### **Input**
```
6x6:abcDcfDdia
```

### **Execution**
```bash
python unruly_solver.py
```

### **Output**
Initial Board:
```
0 - 0 - - 0
- - - 1 - -
0 - - - - -
0 - - - 1 -
- - 0 - - -
- - - - - 0
```

Final Board:
```
0 1 0 1 1 0
1 0 0 1 0 1
0 1 1 0 0 1
0 1 1 0 1 0
1 0 0 1 0 1
1 0 1 0 1 0
```

Violations: 0  
Steps made: 22
Execution Time: 2.35 seconds  

