import { useState, useEffect } from "react";
import SudokuGrid from "./sudokuGrid";
import { Button } from "./ui/button";
import { getSudoku } from "sudoku-gen";
import { interpretSudokuPuzzle } from "@/functions/getSudokuGrid";
import { interpretTextFile } from "@/functions/interpretTextFile";
import ModalProvider from "@/providers/modal-provider";
import axios from "axios";

const Sudoku = () => {
  const [grid, setGrid] = useState<number[][]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  useEffect(() => {
    const sudoku = getSudoku();
    setGrid(interpretSudokuPuzzle(sudoku.puzzle));
  }, []);

  const handleReset = () => {
    const sudoku = getSudoku();
    setGrid(interpretSudokuPuzzle(sudoku.puzzle));
  };

  const handleInputChange = (
    rowIndex: number,
    cellIndex: number,
    value: string
  ) => {
    const newGrid = grid.map((row, rIdx) =>
      row.map((cell, cIdx) =>
        rIdx === rowIndex && cIdx === cellIndex ? parseInt(value, 10) : cell
      )
    );
    setGrid(newGrid);
  };

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (file) {
      try {
        const textGrid = await interpretTextFile(file);
        setGrid(textGrid);
      } catch (error) {
        setError(
          "Error interpreting the text file. Please check the file format."
        );
        setIsDialogOpen(true);
      }
    }
  };

  const closeDialog = () => {
    setIsDialogOpen(false);
    setError(null);
  };

  const handleCheck = async () => {
    try {
      const response = await axios.post("http://localhost:5000/check", {
        grid,
      });
      const { valid, solvedGrid } = response.data;
      console.log(response.data);
      if (valid) {
        console.log("The Sudoku grid is valid!");
        setGrid(solvedGrid);
      } else {
        console.log("The Sudoku grid is invalid.");
      }
    } catch (error) {
      console.error("Error checking Sudoku grid:", error);
      alert("There was an error checking the Sudoku grid.");
    }
  };

  return (
    <div>
      <SudokuGrid grid={grid} onInputChange={handleInputChange} />
      <div className="grid grid-cols-2 gap-2 grid-rows-2 mt-4">
        <Button onClick={handleCheck}>Check</Button>
        <Button variant="destructive" onClick={handleReset}>
          Reset
        </Button>
        <Button
          className="col-span-2"
          onClick={() => document.getElementById("fileInput")?.click()}
        >
          Upload from text file
        </Button>
        <input
          id="fileInput"
          type="file"
          accept=".txt"
          style={{ display: "none" }}
          onChange={handleFileUpload}
        />
      </div>
      <ModalProvider
        error={error}
        isOpen={isDialogOpen}
        onClose={closeDialog}
      />
    </div>
  );
};

export default Sudoku;