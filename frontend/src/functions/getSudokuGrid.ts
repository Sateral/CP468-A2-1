export const interpretSudokuPuzzle = (puzzle: string): number[][] => {
  const grid: number[][] = [];
  for (let i = 0; i < 9; i++) {
    const row: number[] = [];
    for (let j = 0; j < 9; j++) {
      const char = puzzle[i * 9 + j];
      row.push(char === "-" ? 0 : parseInt(char, 10));
    }
    grid.push(row);
  }
  return grid;
};
