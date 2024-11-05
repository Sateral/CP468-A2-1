import "../App.css"; // Make sure to create and style this CSS file

const SudokuGrid = ({
  grid,
  onInputChange,
}: {
  grid: number[][];
  onInputChange: (rowIndex: number, cellIndex: number, value: string) => void;
}) => {
  return (
    <div className="sudoku-grid">
      {grid.map((row, rowIndex) => (
        <div key={rowIndex} className="sudoku-row">
          {row.map((cell, cellIndex) => (
            <input
              key={cellIndex}
              className="sudoku-cell text-center"
              type="text"
              value={
                grid[rowIndex][cellIndex] === 0 ? "" : grid[rowIndex][cellIndex]
              }
              pattern="[1-9]"
              maxLength={1}
              onChange={(e) => {
                const value = e.target.value;
                if (value.match(/^[1-9]$/)) {
                  onInputChange(rowIndex, cellIndex, value);
                } else if (value === "") {
                  onInputChange(rowIndex, cellIndex, "0");
                }
              }}
            />
          ))}
        </div>
      ))}
    </div>
  );
};

export default SudokuGrid;
