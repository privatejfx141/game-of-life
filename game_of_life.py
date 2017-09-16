BIRTH, SURVIVAL = 'B', 'S'
DEAD, ALIVE, SPACE = '.', 'o', ' '

RULES = {
    'life': 'B3/S23',
    'pseudorandom': 'B25/S4',
    'seeds': 'B2/S',
    'replicator': 'B1357/S1357',
    'inkspot': 'B3/S012345678',
    '34life': 'B34/S34',
    'diamoeba': 'B35678/S5678',
    '2x2': 'B36/S125',
    'highlife': 'B36/S23',
    'daynight': 'B3678/S34678',
    'morley': 'B368/S245',
    'anneal': 'B4678/S35678'
}


class Grid:
    """Sparse matrix representation of Conway's Game of Life."""

    def __init__(self, rows, cols, rule=None):
        """(Grid, int, int[, str]) -> NoneType

        Create a Game of Life grid with the given rows and columns.

        REQ: rows, cols > 5
        """
        self._rows = rows
        self._cols = cols
        self._alive = set()
        if not rule:
            self._rule = {BIRTH: [3], SURVIVAL: [2, 3]}
        else:
            self.set_rule(rule)

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

    def num_rows(self):
        """(Grid) -> int

        Return the number of rows of this grid.
        """
        return self._rows

    def num_cols(self):
        """(Grid) -> int

        Return the number of columns of this grid.
        """
        return self._cols

    def set_rule(self, rule):
        """(Grid, str) -> NoneType

        Set the cellular automaton rule.
        """
        b, s = rule.split('/')
        b_values = list(map(int, list(b[1:])))
        s_values = list(map(int, list(s[1:])))
        self._rule = {BIRTH: b_values, SURVIVAL: s_values}

    def get_rule(self):
        """(Grid) -> str

        Return the string representation of the cellular automaton rule.
        """
        b = BIRTH + ''.join(list(map(str, self._rule[BIRTH])))
        s = SURVIVAL + ''.join(list(map(str, self._rule[SURVIVAL])))
        return b + '/' + s

    def set_cells(self, *cells):
        """(Grid, tuple of (int, int)) -> NoneType

        Set the living cells of this grid.
        """
        self._alive = set(cells)

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
        return self._alive.copy() if by_value else self._alive

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
                # Get number of alive neighbours.
                nbs = len(self._alive.intersection(self.neighbours(*cell)))
                # (default: B3/S23)
                is_alive = nbs in self._rule[BIRTH] or (
                    nbs in self._rule[SURVIVAL] and cell in self._alive)
                if is_alive:
                    new_cells.add(cell)

            # Set the new cells.
            self._alive = new_cells

        return self

    def add_pattern(self, pattern, r=None, c=None):
        """(Grid, list of list, int, int)

        Add a pattern to this grid. If r and c are not specified,
        add a pattern to the center of this grid.
        """
        # Get pattern dimensions.
        height, width = len(pattern), len(pattern[0])
        # If no r, c values are specific, get the centre of the grid.
        if not (r and c):
            r = self._rows // 2
            c = self._cols // 2
        # Loop and add the living cells onto the board.
        for h in range(height):
            for w in range(width):
                if pattern[h][w] == 1:
                    self._alive.add(((r+h-(height//2)) % self._rows,
                                     (c+w-(width//2)) % self._cols))


if __name__ == '__main__':
    board = Grid(10, 10)
    glider = [[0, 1, 0], [0, 0, 1], [1, 1, 1]]
    board.add_pattern(glider, 1, 1)

    print(board)
    print('-' * 20)
    print(board.step(100))
