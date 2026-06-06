"""A Python-based application that solves 9x9 Sudoku puzzles using a classic
backtracking algorithm, featuring a dynamic, real-time terminal-based visu-
alization of the solving process.
"""

from Sudoku import Sudoku

if __name__ == "__main__":
    sudoku = Sudoku.fromFile("board.txt")
    sudoku.printBoard()
    sudoku.solveSudoku()
