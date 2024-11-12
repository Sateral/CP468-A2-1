from collections import deque

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


def parse_sudoku(input_file):
   """Read a Sudoku puzzle from a text file and set up initial domains.
  
   Each cell in the Sudoku puzzle has a "domain" – possible values it can take.
   If a cell is empty (represented by '0'), it has the domain {1, 2, ..., 9}.
   If a cell has a fixed number, its domain is that single number.
   """
   domains = {}  # Dictionary to store possible values for each cell
   with open(input_file, 'r') as file:
       for i, line in enumerate(file):
           for j, value in enumerate(line.strip().split()):
               if value == '0':  # Empty cell
                   domains[(i, j)] = set(range(1, 10))  # All values are possible
               else:
                   domains[(i, j)] = {int(value)}  # Fixed cell with a single value
   return domains
def get_neighbors(var):
   """Return all neighbors of a variable (row, column, and subgrid constraints).
  
   Neighbors are cells that share a row, column, or 3x3 subgrid with the given cell.
   """
   row, col = var
   neighbors = set()
   # Add all cells in the same row and column
   for k in range(9):
       if k != col:
           neighbors.add((row, k))  # Cells in the same row
       if k != row:
           neighbors.add((k, col))  # Cells in the same column
   # Add cells in the same 3x3 subgrid
   start_row, start_col = 3 * (row // 3), 3 * (col // 3)
   for r in range(start_row, start_row + 3):
       for c in range(start_col, start_col + 3):
           if (r, c) != var:
               neighbors.add((r, c))
              
   return neighbors
def ac3(domains):
   """Enforce arc-consistency using the AC-3 algorithm.
  
   AC-3 algorithm iteratively enforces consistency between pairs of cells.
   It removes values from the domains if they conflict with neighbors.
   """
   # Initialize the queue with all pairs of cells that have constraints
   queue = deque((X, Y) for X in domains for Y in get_neighbors(X))
   queue_lengths = [len(queue)]  # Track queue length at each step
   while queue:
       (X, Y) = queue.popleft()
       revised = revise(domains, X, Y)
      
       # If revising the domain results in an empty domain, return failure
       if revised:
           if len(domains[X]) == 0:
               return False, queue_lengths  # Return failure due to empty domain
           # Add neighbors of X back into the queue, excluding Y to avoid duplicate checks
           for Z in get_neighbors(X) - {Y}:
               queue.append((Z, X))
              
       queue_lengths.append(len(queue))
   return True, queue_lengths  # Return success and queue length tracking
def revise(domains, X, Y):
   """Revise the domain of X to satisfy arc-consistency with Y.
  
   Removes values from the domain of X if they don't satisfy constraints with Y.
   """
   revised = False
   for x in set(domains[X]):  # Use a copy to safely modify domains[X] while iterating
       if all(x == y for y in domains[Y]):
           domains[X].remove(x)  # Remove value if it conflicts with all values in Y's domain
           revised = True
   return revised
def is_solved(domains):
   """Check if the CSP (Sudoku puzzle) is completely solved.
  
   A puzzle is solved if each cell has exactly one possible value.
   """
   return all(len(domains[cell]) == 1 for cell in domains)
def get_solution(domains):
   """Convert the domains to a 9x9 solved grid if the puzzle is solved.
  
   Each cell in the solved grid will contain the single value left in its domain.
   """
   solution = [[0] * 9 for _ in range(9)]
   for (row, col), domain in domains.items():
       solution[row][col] = next(iter(domain))  # Get the single value in the domain
   return solution
def backtrack(domains):
   """Backtracking search with constraint propagation."""
   if is_solved(domains):
       return domains
  
   # Select an unassigned cell with the smallest domain (minimum remaining values heuristic)
   unassigned = [cell for cell in domains if len(domains[cell]) > 1]
   cell = min(unassigned, key=lambda x: len(domains[x])) #MRV Heuristic
  
   # Try each possible value in the selected cell's domain
   original_domain = domains[cell].copy()
   for value in original_domain:
       new_domains = {k: v.copy() for k, v in domains.items()}
       new_domains[cell] = {value}
      
       # Apply AC-3 with the updated assignment
       result, _ = ac3(new_domains)
       if result:
           # Recurse with the new domain state
           solution = backtrack(new_domains)
           if solution:
               return solution
  
   #if a solution is not found, then backtrack
   return None
def display_solution(solution):
   """Display the Sudoku solution in a readable 9x9 format."""
   for row in solution:
       print(" ".join(map(str, row)))
# Example: To solve a Sudoku puzzle from 'input.txt'
def solve_sudoku(input_file):
   """Main function to solve the Sudoku using AC-3 and constraint propagation if needed."""
   # Parse the initial Sudoku puzzle and set up the domains
   domains = parse_sudoku_from_matrix(input_file)
  
   # Apply the AC-3 algorithm to reduce domains through arc-consistency
   result, queue_lengths = ac3(domains)
  
   # Report the queue lengths after each step for debugging or analysis
   print("Queue lengths at each step:", queue_lengths)
  
   # Check if AC-3 solved the puzzle entirely
   if is_solved(domains):
        print("The puzzle is solved by AC-3 alone.")

        return True, get_solution(domains), "The puzzle is solved by AC-3 alone."

   else:
       print("AC-3 did not completely solve the puzzle.")
       # Additional solving with constraint propagation could be added here if needed
       solution = backtrack(domains)
       if solution:
           print("The puzzle is solved with backtracking.")
           return True, get_solution(solution), "The puzzle is solved with backtracking."
       else:
            print("The puzzle could not be solved.")
            return False, None, "The puzzle could not be solved."
# Sample puzzle creation for testing
def create_sudoku_input(filename, puzzle):
   """Write a sample 9x9 Sudoku puzzle to a text file in the required format."""
   with open(filename, 'w') as file:
       for row in puzzle:
           file.write(" ".join(map(str, row)) + "\n")
