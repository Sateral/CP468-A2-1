export function interpretTextFile(file: File) {
  return new Promise<number[][]>((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const lines = (reader.result as string)
        .split("\n")
        .map((line) => line.trim());

      // Check if the file has exactly 9 lines
      if (lines.length !== 9) {
        return reject(new Error("The file must contain exactly 9 lines."));
      }

      const result = lines.map((line) => {
        const numbers = line.split("").map(Number);

        // Check if each line has exactly 9 numbers
        if (numbers.length !== 9) {
          throw new Error("Each line must contain exactly 9 numbers.");
        }

        // Check if each number is between 0 and 9
        for (const num of numbers) {
          if (isNaN(num) || num < 0 || num > 9) {
            throw new Error("Each cell must be a number between 0 and 9.");
          }
        }

        return numbers;
      });

      resolve(result);
    };
    reader.onerror = () => reject(reader.error);
    reader.readAsText(file);
  });
}
