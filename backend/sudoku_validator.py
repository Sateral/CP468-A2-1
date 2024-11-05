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

def validate_sudoku(grid):
    # for row in grid:
    #     print(f"{row}\n")
    return True, grid