import sys
import time

class UnrulySolver:
    """Class to solve Unruly puzzles."""

    def __init__(self, input_file, max_nodes , heuristically = False):
        """Initialize the solver with the input file and max nodes."""

        self.input_file = input_file
        self.heuristically = heuristically
        self.max_nodes = max_nodes
        self.board = []
        self.n = 0
        self.m = 0
        self.expanded_nodes = 0
        self.solution = None


    def parse_input(self):
        """Reads the input file and creates the Unruly Board."""

        with open(self.input_file, 'r') as f:
            data = f.read().strip()

        # Decode size and data
        size, encoded_positions = data.split(':')
        self.n, self.m = map(int, size.split('x'))

        if self.n % 2 or self.m % 2: # if any of n or m are not even , exit
            sys.exit(-1)

        # Initialize Board structure
        self.board = [['-' for _ in range(self.m)] for _ in range(self.n)]

        # Decode Positions
        current_index = 0
        for char in encoded_positions:
            step = ord(char.lower()) - ord('a') + 1 # create the step using the char provided as step
            current_index += step
            row, col = divmod(current_index - 1, self.m)
            if row < self.n:
                self.board[row][col] = '1' if char.isupper() else '0'


    def is_valid(self, row, col, color):
        """Checks if the color provided in (row,col) cell is valid."""

        # Color the cell
        self.board[row][col] = color

        #1. Check for 3 consecutive colors

        # check horizontally
        for r in range(self.n):
            for c in range(self.m - 2):
                if self.board[r][c] == self.board[r][c + 1] == self.board[r][c + 2] == color: # 3 consecutive colors found!
                    self.board[row][col] = '-'
                    return False

        # check vertically
        for c in range(self.m):
            for r in range(self.n - 2):
                if self.board[r][c] == self.board[r + 1][c] == self.board[r + 2][c] == color:
                    self.board[row][col] = '-'
                    return False

        #2. Check for color balance in the whole board (#whites = #blacks in every row,col)
        for r in range(self.n):
            if self.board[r].count('1') > self.m // 2 or self.board[r].count('0') > self.m // 2:
                self.board[row][col] = '-'
                return False

        for c in range(self.m):
            col_values = [self.board[r][c] for r in range(self.n)]
            if col_values.count('1') > self.n // 2 or col_values.count('0') > self.n // 2:
                self.board[row][col] = '-'
                return False

        # All constraints are satisfied!
        self.board[row][col] = '-'
        return True


    def solve(self, row=0, col=0):
        """Solve Unruly problem as a CSP using backtracking."""

        if self.expanded_nodes > self.max_nodes:
            return False

        # if we reach the end of the board
        if row == self.n:
            self.solution = [''.join(row) for row in self.board]
            return True

        # Find next board cell
        next_row, next_col = (row, col + 1) if col + 1 < self.m else (row + 1, 0)

        # if cell is already colored , move to next board cell
        if self.board[row][col] != '-':
            return self.solve(next_row, next_col)

        # Try to color the cell
        for color in ['0', '1']:
            if self.is_valid(row, col, color):
                self.board[row][col] = color
                self.expanded_nodes += 1
                if self.solve(next_row, next_col):
                    return True
                self.board[row][col] = '-'  # remove color on failure

        return False


    def write_solution(self, output_file):
      """Write the solution to an output file with correct encoding."""

      if self.solution:
          with open(output_file, 'w') as f:
              # first we write the size of the matrix n x m
              size = f"{self.n}x{self.m}"

              # encode the solution from 01 to aA
              encoded_solution = []
              for cell in ''.join(self.solution):
                  if cell == '0':  # white cell
                      encoded_solution.append('a')
                  elif cell == '1':  # black cell
                      encoded_solution.append('A')

              # Add the ending stopword small a
              encoded_solution.append('a')

              # write the solution to the file
              f.write(f"{size}:{''.join(encoded_solution)}")
      else:
          print("No solution found!")


    def run(self):
        self.parse_input()
        print("Initial board(0 for white , 1 for black):")
        for row in self.board:
            print(' '.join(row))

        start_time = time.time()

        solved = self.solve_heuristic() if self.heuristically else self.solve()
        end_time = time.time()

        if solved:
            print("\nSolution found!")
            for row in self.solution:
                print(' '.join(row))
        else:
            if self.expanded_nodes > self.max_nodes:
              print("\nNo solution exists for the specified max number of nodes.")
            else:
              print("\nNo solution exists.")

        print(f"Time taken: {end_time - start_time:.2f} seconds")
        print(f"Nodes expanded: {self.expanded_nodes}")


    """ **************************BONUS PART**************************"""

    def apply_heuristics(self, row, col):
      """Apply heuristic rules to fill certain cells deterministically."""
      changes = []  # Track all changes made by heuristics

      # Check horizontal row
      for c in range(self.m - 2):
          # Rule: If two consecutive are the same, fill before and after with the opposite color
          if self.board[row][c] == self.board[row][c + 1] != '-':
              if c - 1 >= 0 and self.board[row][c - 1] == '-':
                  self.board[row][c - 1] = '0' if self.board[row][c] == '1' else '1'
                  changes.append((row, c - 1))
              if c + 2 < self.m and self.board[row][c + 2] == '-':
                  self.board[row][c + 2] = '0' if self.board[row][c] == '1' else '1'
                  changes.append((row, c + 2))

          # Rule: If one empty between two same colors, fill it with the opposite color
          if c + 2 < self.m and self.board[row][c] == self.board[row][c + 2] != '-' and self.board[row][c + 1] == '-':
              self.board[row][c + 1] = '0' if self.board[row][c] == '1' else '1'
              changes.append((row, c + 1))

      # Check vertical column
      for r in range(self.n - 2):
          # Rule: If two consecutive are the same, fill before and after with the opposite color
          if self.board[r][col] == self.board[r + 1][col] != '-':
              if r - 1 >= 0 and self.board[r - 1][col] == '-':
                  self.board[r - 1][col] = '0' if self.board[r][col] == '1' else '1'
                  changes.append((r - 1, col))
              if r + 2 < self.n and self.board[r + 2][col] == '-':
                  self.board[r + 2][col] = '0' if self.board[r][col] == '1' else '1'
                  changes.append((r + 2, col))

          # Rule: If one empty between two same colors, fill it
          if r + 2 < self.n and self.board[r][col] == self.board[r + 2][col] != '-' and self.board[r + 1][col] == '-':
              self.board[r + 1][col] = '0' if self.board[r][col] == '1' else '1'
              changes.append((r + 1, col))

      return changes


    def solve_heuristic(self, row=0, col=0):
        """Solve Unruly problem as a CSP using backtracking with heuristics."""

        if self.expanded_nodes > self.max_nodes:
            return False

        # if we reach the end of the board
        if row == self.n:
            self.solution = [''.join(row) for row in self.board]
            return True

        # Find next board cell
        next_row, next_col = (row, col + 1) if col + 1 < self.m else (row + 1, 0)

        # If cell is already colored, move to next
        if self.board[row][col] != '-':
            heuristic_changes = self.apply_heuristics(row, col)
            if self.solve_heuristic(next_row, next_col):
                return True
            # Undo heuristic changes if backtracking
            for r, c in heuristic_changes:
                self.board[r][c] = '-'
            return False

        # Try to color the cell
        for color in ['0', '1']:
            if self.is_valid(row, col, color):
                self.board[row][col] = color
                self.expanded_nodes += 1
                heuristic_changes = self.apply_heuristics(row, col)  # Apply heuristics after coloring
                if self.solve_heuristic(next_row, next_col):
                    return True
                # Undo heuristic changes and color if backtracking
                for r, c in heuristic_changes:
                    self.board[r][c] = '-'
                self.board[row][col] = '-'  # remove color on failure

        return False





if __name__ == '__main__':
    file_name = input("Enter the input file name: ")
    max_nodes = int(input("Enter the maximum number of nodes to expand: "))
    solver = UnrulySolver(input_file = file_name , max_nodes = max_nodes , heuristically = True) # specify if you want to use heiristic methods for the solution or not.
    solver.run()
    solver.write_solution('out.txt')
