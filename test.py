from collections import deque

def parse_sudoku(input_file):
   """Read a Sudoku puzzle from a text file and set up initial domains."""
   domains = {}
   with open(input_file, 'r') as file:
       for i, line in enumerate(file):
           for j, value in enumerate(line.strip().split()):
               if value == '0':
                   domains[(i, j)] = set(range(1, 10))
               else:
                   domains[(i, j)] = {int(value)}
   return domains

def parse_sudoku_from_matrix(matrix):
    """Read a Sudoku puzzle from a 2D matrix and set up initial domains."""
    domains = {}
    for i in range(9):
        for j in range(9):
            value = matrix[i][j]
            if value == 0:
                domains[(i, j)] = set(range(1, 10))
            else:
                domains[(i, j)] = {value}
    return domains

def get_neighbors(var):
   """Return all neighbors of a variable (row, column, and subgrid constraints)."""
   row, col = var
   neighbors = set()
   for k in range(9):
       if k != col:
           neighbors.add((row, k))  # same row
       if k != row:
           neighbors.add((k, col))  # same column
  
   # same 3x3 subgrid
   start_row, start_col = 3 * (row // 3), 3 * (col // 3)
   for r in range(start_row, start_row + 3):
       for c in range(start_col, start_col + 3):
           if (r, c) != var:
               neighbors.add((r, c))
   return neighbors
def ac3(domains):
   """Enforce arc-consistency using the AC-3 algorithm."""
   queue = deque((X, Y) for X in domains for Y in get_neighbors(X))
   queue_lengths = [len(queue)]  # Track queue length at each step
  
   while queue:
       (X, Y) = queue.popleft()
       revised = revise(domains, X, Y)
       if revised:
           if len(domains[X]) == 0:
               return False, queue_lengths  # Failure due to empty domain
           for Z in get_neighbors(X) - {Y}:
               queue.append((Z, X))
       queue_lengths.append(len(queue))
  
   return True, queue_lengths
def revise(domains, X, Y):
   """Revise the domain of X to satisfy arc-consistency with Y."""
   revised = False
   for x in set(domains[X]):
       if all(x == y for y in domains[Y]):
           domains[X].remove(x)
           revised = True
   return revised
def is_solved(domains):
   """Check if the CSP is completely solved."""
   return all(len(domains[cell]) == 1 for cell in domains)
def get_solution(domains):
   """Convert the domains to a 9x9 solved grid if solved."""
   solution = [[0] * 9 for _ in range(9)]
   for (row, col), domain in domains.items():
       solution[row][col] = next(iter(domain))
   return solution
def display_solution(solution):
   """Display the Sudoku solution in a readable format."""
   for row in solution:
       print(" ".join(map(str, row)))


# Example: To solve a Sudoku puzzle from 'input.txt'
def solve_sudoku(input_file):
    """Main function to solve the Sudoku using AC-3 and constraint propagation if needed."""
    domains = parse_sudoku_from_matrix(input_file)
    result, queue_lengths = ac3(domains)
    
    # Report queue lengths
    print("Queue lengths at each step:", queue_lengths)
    
    # Check if AC-3 solved the puzzle
    if is_solved(domains):
        print("The puzzle is solved by AC-3 alone.")
        display_solution(get_solution(domains))
    else:
        print("AC-3 did not completely solve the puzzle.")
        # Additional solving with constraint propagation if necessary


if __name__ == "__main__":
   # Example 9x9 Sudoku puzzle
   sample_puzzle = [
       [5, 3, 0, 0, 7, 0, 0, 0, 0],
       [6, 0, 0, 1, 9, 5, 0, 0, 0],
       [0, 9, 8, 0, 0, 0, 0, 6, 0],
       [8, 0, 0, 0, 6, 0, 0, 0, 3],
       [4, 0, 0, 8, 0, 3, 0, 0, 1],
       [7, 0, 0, 0, 2, 0, 0, 0, 6],
       [0, 6, 0, 0, 0, 0, 2, 8, 0],
       [0, 0, 0, 4, 1, 9, 0, 0, 5],
       [0, 0, 0, 0, 8, 0, 0, 7, 9]
   ]
  
   solve_sudoku(sample_puzzle)