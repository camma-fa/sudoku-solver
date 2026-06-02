class Solution:
    @staticmethod
    def getBoxIndex(r: int, c: int) -> int:
        """Computes the index of the box to which the cell (r, c) belongs.
        The boxes are numbered from 0 to 8, starting from the top-left.

        Args:
            r (int): The row index of the cell.
            c (int): The column index of the cell.

        Returns:
            int: The index of the box to which the cell belongs.
        """
        return (r // 3) * 3 + (c // 3)

    def solveSudoku(self, board: list[list[str]]) -> None:
        # Hash tables to keep track of the numbers present in each row, column
        # and box
        rows_ht = [set() for _ in range(9)]
        cols_ht = [set() for _ in range(9)]
        boxes_ht = [set() for _ in range(9)]

        # List to store the coordinates (rows, cols, boxes) of empty cells
        empty_cells = []

        # Iterate through the board to fill the hash tables and identify empty
        # cells
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    empty_cells.append((r, c, self.getBoxIndex(r, c)))
                else:
                    rows_ht[r].add(board[r][c])
                    cols_ht[c].add(board[r][c])
                    b = self.getBoxIndex(r, c)
                    boxes_ht[b].add(board[r][c])

        def backtrack(index: int) -> bool:
            """Backtracking function to fill the empty cells.

            Args:
                index (int): The index of the current empty cell.

            Returns:
                bool: True if a solution is found, False otherwise.
            """
            # Base case: if we have filled all empty cells, the board is solved
            if index == len(empty_cells):
                return True

            # Get the coordinates of the current empty cell
            r, c, b = empty_cells[index]

            # Try each number from 1 to 9 in the current empty cell
            for n in "123456789":
                # Check if the number is already present in the current row,
                # column or box. If it is, skip to the next number, otherwise
                # place the number in the cell and update the hash tables
                if n in rows_ht[r] or n in cols_ht[c] or n in boxes_ht[b]:
                    continue
                else:
                    board[r][c] = n
                    rows_ht[r].add(n)
                    cols_ht[c].add(n)
                    boxes_ht[b].add(n)

                # Recursively call backtrack for the next empty cell. If it re-
                # turns True, we have found a solution and can return True, oth-
                # erwise we need to backtrack by removing the number from the
                # cell and updating the hash tables
                if backtrack(index + 1):
                    return True
                board[r][c] = "."
                rows_ht[r].remove(n)
                cols_ht[c].remove(n)
                boxes_ht[b].remove(n)

            # If we have tried all numbers and none of them lead to a solution,
            # return False to backtrack
            return False

        # Start the backtracking process from the first empty cell
        backtrack(0)
