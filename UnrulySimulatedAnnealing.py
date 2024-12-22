import random
from datetime import datetime
import math
import sys
import time


class UnrulySolver:

    def __init__(self, input_file, max_steps):
        self.input_file = input_file
        self.max_steps = max_steps
        self.board = []
        self.fixed_positions = set()  # (row, col) for fixed values
        self.n = 0 # rows
        self.m = 0 # cols
        random.seed(datetime.now().timestamp()) # initialize the seed


    def parse_input(self):
        """Reads the input file and creates the Unruly Board."""
        with open(self.input_file, 'r') as f:
            data = f.read().strip()

        size, encoded_positions = data.split(':')
        self.n, self.m = map(int, size.split('x'))

        if self.n % 2 or self.m % 2:  # If any of n or m are not even, exit
            sys.exit("Board dimensions must be even!")

        # Initialize board structure
        self.board = [['-' for _ in range(self.m)] for _ in range(self.n)]

        # Decode Positions
        current_index = 0
        for char in encoded_positions:
            step = ord(char.lower()) - ord('a') + 1
            current_index += step
            row, col = divmod(current_index - 1, self.m)
            if row < self.n:
                self.board[row][col] = '1' if char.isupper() else '0'
                self.fixed_positions.add((row, col))


    def fill_random(self):
        """Fill the empty cells ('-') in the board randomly with 0 or 1."""
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j] == '-':
                    self.board[i][j] = random.choice(['0', '1'])


    def objective_function(self, board):
        """Calculate the objective value of a board state."""

        """The objective function is defined as follows: Sum ( f(s) ) """

        """For each state f(s) = sum_i=1_n(rbi - rwi) + sum_j=1_m(cbj + cwj) + sum_i=1_n(tri) + sum_j=1_m(trj)"""

        """rbi , rwi , cbj , cwj μετράνε το πλήθος των μαύρων/άσπρων τετραγώνων στην γραμμή i και στη"""

        """στήλη j αντίστοιχα, ενώ τα tri , trj μετράνε το πλήθος των τριάδων συνεχόμενων τετραγώνων με το"""

        """ίδιο χρώμα στην γραμμή i και στη στήλη j αντίστοιχα"""

        violations = 0

        # Row and column constraints
        for i in range(self.n):
            row = board[i]
            row_zeros = row.count('0') # rbi
            row_ones = row.count('1')  # rwi
            violations += abs(row_zeros - row_ones)

        for j in range(self.m):
            col = [board[i][j] for i in range(self.n)]
            col_zeros = col.count('0')
            col_ones = col.count('1')
            violations += abs(col_zeros - col_ones)

        # Consecutive 3+ same color violations
        for i in range(self.n):
            for j in range(self.m - 2):
                if board[i][j] == board[i][j + 1] == board[i][j + 2]:
                    violations += 1

        for j in range(self.m):
            for i in range(self.n - 2):
                if board[i][j] == board[i + 1][j] == board[i + 2][j]:
                    violations += 1

        return violations


    def random_successor(self, state):
        """Select a random successor by flipping a non-fixed cell."""
        while True:
            i = random.randint(0, self.n - 1)
            j = random.randint(0, self.m - 1)
            if (i, j) not in self.fixed_positions: # make sure that you do not change a predefined position!
                new_state = [row[:] for row in state]
                new_state[i][j] = '1' if state[i][j] == '0' else '0'
                return new_state


    def simulated_annealing(self):
        """Perform simulated annealing to minimize violations."""

        def exp_schedule(t):
            """Exponential decay schedule."""

            """ To ensure the temperature T approaches zero close to the end of the allowed steps, """

            """ we need to scale the cooling schedule to match the maximum number of steps."""

            k = math.log(1 / 0.01) / self.max_steps  # Calculate decay rate
            return max(0.01 , 1 * math.exp(-k * t))  # Ensure T does not go below 0.01



        current_state = [row[:] for row in self.board]
        current_value = self.objective_function(current_state)
        best_state = current_state # assume that current state is the best for now
        best_value = current_value

        for t in range(self.max_steps):
            T = exp_schedule(t)
            if T == 0.01:
                break

            if self.objective_function(current_state) == 0:
                break

            next_state = self.random_successor(current_state)
            next_value = self.objective_function(next_state)
            delta_e = next_value - current_value

            # NOTE: delta_e < 0 means we have a better new state (because we minimize the f function)

            # If new_state is better accept it , or if its not but we have to accept it probabillistically
            if delta_e < 0 or random.uniform(0, 1) < math.exp(-delta_e / T): # we have -delta_e because we want to minimize , not maximize the f function
                current_state = next_state
                current_value = next_value

                # track the best state found!
                if current_value < best_value:
                    best_state = current_state
                    best_value = current_value

        self.board = best_state
        return best_value , t + 1


    def print_board(self):
        """Print the current board."""
        for row in self.board:
            print(' '.join(row))


    def write_solution(self, output_file):
      """Write the solution to an output file with correct encoding."""
      with open(output_file, 'w') as f:
        # first we write the size of the matrix n x m
        size = f"{self.n}x{self.m}"

        # encode the solution from 01 to aA
        encoded_solution = []
        for cell in ''.join(self.board):
          if cell == '0':  # white cell
            encoded_solution.append('a')
          elif cell == '1':  # black cell
            encoded_solution.append('A')

        # Add the ending stopword small a
        encoded_solution.append('a')

        # write the solution to the file
        f.write(f"{size}:{''.join(encoded_solution)}")


def main():
    input_file = input("Enter the input file name: ")
    max_steps = int(input("Enter the maximum number of steps: "))
    solver = UnrulySolver(input_file, max_steps)

    start_time = time.time()
    solver.parse_input()
    solver.fill_random()
    print("Initial Board:")
    solver.print_board()
    print(f"\nViolations: {solver.objective_function(solver.board)}")

    best_value , steps_made = solver.simulated_annealing()
    end_time = time.time()

    print("\nFinal Board:")
    solver.print_board()
    print(f"\nViolations: {best_value}")
    print(f"Steps made:{steps_made}")
    print(f"Execution Time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
