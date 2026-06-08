import sys
import time


class Sudoku:
    """A class that provides methods to solve a 9x9 Sudoku puzzle using a back-
    tracking algorithm, as well as to print the board in a visually appealing
    format.
    """

    def __init__(self, board: list[list[str]]) -> None:
        """Constructor for the Sudoku class.

        Args:
            board (list[list[str]]): The initial state of the Sudoku board.
        """
        self.__board = board

        # Hash tables to keep track of the numbers present in each row, column
        # and box
        self.__rows_ht = [set() for _ in range(9)]
        self.__cols_ht = [set() for _ in range(9)]
        self.__boxes_ht = [set() for _ in range(9)]

        # List to store the coordinates (row, col, box) of empty cells
        self.__empty_cells = []

        self.__initializeStructures()

        # Constants for board printing
        self.__DELAY = 0.002
        self.__EMPTY_CELL_CHAR = " "
        self.__EMPTY_CELL_COLOR = "\033[1;32m"
        self.__FIXED_DIGIT_COLOR = "\033[1;37m"
        self.__TRY_DIGIT_COLOR = "\033[1;31m"

    @classmethod
    def fromFile(cls, file_path: str) -> "Sudoku":
        """Creates a Sudoku instance from a text file.\n
        The file should contain 9 lines, each with 9 characters (digits or dots
        for empty cells) separated by spaces.

        Args:
            file_path (str): The path to the text file containing the Sudoku
            board.

        Returns:
            Sudoku: An instance of the Sudoku class initialized with the board
            from the file.
        """
        with open(file_path, "r") as f:
            board = [list(line.strip().split()) for line in f.readlines()]

        # Return an instance of the Sudoku class initialized with the loaded
        # board
        return cls(board)

    def __getBoxIndex(self, r: int, c: int) -> int:
        """Computes the index of the box which the cell (r, c) belongs to.
        Boxes are numbered from 0 to 8, starting from the top-left one.

        Args:
            r (int): The row index of the cell.
            c (int): The column index of the cell.

        Returns:
            int: The index of the box which the cell belongs to.
        """
        return (r // 3) * 3 + (c // 3)

    def __initializeStructures(self) -> None:
        """Initializes hash tables and the list of empty cells based on the ini-
        tial state of the board.
        """
        for r in range(9):
            for c in range(9):
                b = self.__getBoxIndex(r, c)
                if self.__board[r][c] == ".":
                    self.__empty_cells.append((r, c, b))
                else:
                    self.__rows_ht[r].add(self.__board[r][c])
                    self.__cols_ht[c].add(self.__board[r][c])
                    self.__boxes_ht[b].add(self.__board[r][c])

    def __printCell(self, r: int, c: int, char: str, color: str) -> None:
        """Prints a single cell of the Sudoku board with appropriate coloring.

        Args:
            r (int): The row index of the cell.
            c (int): The column index of the cell.
            char (str): The character to print in the cell.
            color (str): The color to use for printing the cell.
        """
        row_offset = (
            1 + r + (r // 3)
        )  # Add 1 to the row index to account for the top border and r // 3 to
        # account for horizontal borders
        col_offset = (
            1 + 1 + c * 3 + (c // 3)
        )  # Multiply the column index by 3 as each cell is 3 chars wide (e.g.,
        # " 1 "), then add 1 to account for the left border and another 1 for
        # the initial space before the first cell in each row and finally c // 3
        # to account for vertical borders

        # Move the terminal cursor to the position of the cell to be printed
        print(
            f"\033[{row_offset + 1};{col_offset + 1}H", end=""
        )  # ANSI coordinates start at 1, not 0, hence the +1)
        # Print the character with the specified color
        print(f"{color}{char}\033[0m", end=" ")
        # Flush the output buffer to ensure the text is printed immediately
        sys.stdout.flush()

        time.sleep(self.__DELAY)

    def __backtrack(self, index: int) -> bool:
        """Backtracking function to fill empty cells.

        Args:
            index (int): The index of the current empty cell.

        Returns:
            bool: True if a solution is found, False otherwise.
        """
        # Base case: if we have filled all empty cells, the board is solved
        if index == len(self.__empty_cells):
            return True

        # Get the coordinates of the current empty cell
        r, c, b = self.__empty_cells[index]

        # Try each number from 1 to 9 in the current empty cell
        for n in "123456789":
            # Check if the number is already present in the current row, column
            # or box. If it is, skip to the next number, otherwise place the
            # number in the cell and update hash tables
            if (
                n in self.__rows_ht[r]
                or n in self.__cols_ht[c]
                or n in self.__boxes_ht[b]
            ):
                continue
            else:
                self.__board[r][c] = n
                self.__rows_ht[r].add(n)
                self.__cols_ht[c].add(n)
                self.__boxes_ht[b].add(n)
                self.__printCell(r, c, n, self.__TRY_DIGIT_COLOR)

            # Recursively call backtrack for the next empty cell. If it returns
            # True, we have found a solution and can return True, otherwise we
            # need to backtrack by removing the number from the cell and updat-
            # ing hash tables
            if self.__backtrack(index + 1):
                return True
            self.__board[r][c] = "."
            self.__rows_ht[r].remove(n)
            self.__cols_ht[c].remove(n)
            self.__boxes_ht[b].remove(n)
            self.__printCell(r, c, self.__EMPTY_CELL_CHAR, self.__EMPTY_CELL_COLOR)

        # If we have tried all numbers and none of them lead to a solution, re-
        # turn False to backtrack
        return False

    def solveSudoku(self) -> bool:
        """Starts the backtracking process from the first empty cell to solve
        the Sudoku puzzle in-place.

        Returns:
            bool: True if a solution is found, False otherwise.
        """
        success = self.__backtrack(0)

        if success:
            print("\n")  # To prevent the terminal prompt from overlapping the
            # bottom border of the Sudoku board
        else:
            print("\033[2J\033[H", end="")  # Clear the terminal screen
            print("No solution exists for the given Sudoku puzzle.")

        return success

    def printBoard(self) -> None:
        """Prints the Sudoku board in a visually appealing format."""
        # Clear the terminal screen
        print("\033[2J\033[H", end="")

        top_border = "╔═════════╦═════════╦═════════╗"
        mid_border = "╠═════════╬═════════╬═════════╣"
        btm_border = "╚═════════╩═════════╩═════════╝"

        print(top_border)
        for i in range(9):
            row = "║"
            for j in range(9):
                cell_digit = self.__board[i][j]
                cell_color = (
                    self.__FIXED_DIGIT_COLOR
                    if cell_digit != "."
                    else self.__EMPTY_CELL_COLOR
                )
                cell = (
                    f" {cell_color}{cell_digit}\033[0m "
                    if cell_digit != "."
                    else f" {cell_color}{self.__EMPTY_CELL_CHAR}\033[0m "
                )
                row += cell

                if j % 3 == 2:
                    row += "║"
            print(row)

            if i == 2 or i == 5:
                print(mid_border)
        print(btm_border)
