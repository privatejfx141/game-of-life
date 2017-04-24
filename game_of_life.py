DEAD, ALIVE, SPACE = '.', 'o', ' '


class Grid:
    """Sparse matrix representation of Conway's Game of Life."""

    def __init__(self, rows, cols):
        """(Grid, int, int) -> NoneType

        Create a Game of Life grid with the given rows and columns.

        REQ: rows, cols > 5
        """
        self._rows = rows
        self._cols = cols
        self._alive = set()

    def __str__(self):
        """(Grid) -> str

        Return the string representation of this grid.
        """
        result = ''
        for r in range(self._rows):
            for c in range(self._cols):
                if (r, c) in self._alive:
                    result += ALIVE
                else:
                    result += DEAD
                if c != self._cols - 1:
                    result += SPACE
            if r != self._rows - 1:
                result += '\n'
        return result

    def clear(self):
        """(Grid) -> NoneType
        
        Clear this grid of all living cells.
        """
        self._alive = set()

    def dimensions(self):
        """(Grid) -> (int, int)

        Return a tuple of the number of rows and columns.
        """
        return self._rows, self._cols

    def add_cell(self, r, c):
        """(Grid, int, int) -> NoneType

        Add a living cell to this grid.
        """
        self._alive.add((r, c))

    def neighbours(self, r, c):
        """(Grid, int, int) -> int

        Return a set of all neighbours around the cell (r, c).
        """
        rg = (-1, 0, 1)
        return {((r+h) % self._rows, (c+w) % self._cols) for h in rg
                for w in rg if not (h == w == 0)}

    def alive_cells(self, by_value=True):
        """(Grid) -> set of (int, int)

        Return a set of all the living cells on this grid. If by_value, return
        a copy of the set. Otherwise return a pointer (by reference).
        """
        if by_value:
            return self._alive.copy()
        else:
            return self._alive

    def step(self, count=1):
        """(Grid[, int]) -> Grid

        Build the state of this grid at generation count.

        REQ: count >= 0
        """
        # Loop through each generation.
        for generation in range(count):

            # Build the set of cells that could be alive.
            temp = self._alive.copy()
            for r, c in self._alive:
                temp = temp.union(self.neighbours(r, c))

            # Determine which cells live on to the next generation.
            new_cells = set()
            for cell in temp:
                nbs = len(set.intersection(
                    self._alive, self.neighbours(*cell)))
                is_alive = nbs == 3 or (nbs == 2 and cell in self._alive)
                if is_alive:
                    new_cells.add(cell)

            # Set the new cells.
            self._alive = new_cells

        return self

    def add_pattern(self, pattern, r=None, c=None):
        """(Grid, list of list, int, int)

        Add a pattern to this grid. If r and c are not specific,
        add a pattern to the center of this grid.
        """
        # If no r, c values are specific, get the centre of the grid.
        if not (r and c):
            r = self._rows // 2
            c = self._cols // 2
        # Loop and add the living cells onto the board.
        for h in range(len(pattern)):
            for w in range(len(pattern[0])):
                if pattern[h][w] == 1:
                    self._alive.add(((r+h) % self._rows, (c+w) % self._cols))


if __name__ == '__main__':
    board = Grid(10, 10)
    board.add_pattern([[0, 1, 0], [0, 0, 1], [1, 1, 1]], 1, 1)

    print(board)
    print()
    print(board.step(100))
