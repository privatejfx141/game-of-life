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


def fix_pattern(pattern_mtx):
    """(list matrix of int) -> list matrix of int

    Fixes the pattern matrix so that every row of the resultant matrix will be
    of equal length; the result matrix is perfectly rectangular.

    :param pattern_mtx: a matrix of integers representing the pattern
    :return: the fixed pattern matrix
    """
    new_pattern = list()
    max_cell_len = max(map(len, pattern_mtx))
    for cell_line in pattern_mtx:
        new_cell_line = cell_line + ([0] * (max_cell_len - len(cell_line)))
        new_pattern.append(new_cell_line)
    return new_pattern


def rotate_pattern(pattern_mtx, fixed=True):
    """(list matrix of int[, bool]) -> list matrix of int

    Rotates the pattern matrix clockwise.

    :param pattern_mtx: a matrix of integers representing the pattern
    :param fixed: True if all rows of the matrix are of equal length; is rectangular
    :return: the rotated pattern
    """
    if not fixed:
        pattern_mtx = fix_pattern(pattern_mtx)
    new_pattern = [list(row) for row in zip(*pattern_mtx[::-1])]
    return new_pattern


def transpose_pattern(pattern_mtx, fixed=True):
    """(list matrix of int[, bool]) -> list matrix of int

    Transposes the pattern matrix.

    :param pattern_mtx: a matrix of integers representing the pattern
    :param fixed: True if all rows of the matrix are of equal length; is rectangular
    :return: the diagonally flipped or transposed pattern
    """
    if not fixed:
        pattern_mtx = fix_pattern(pattern_mtx)
    new_pattern = [list(row) for row in zip(*pattern_mtx)]
    return new_pattern


def flip_horizontal_pattern(pattern_mtx, fixed=True):
    """(list matrix of int[, bool]) -> list matrix of int

    Horizontally flips the pattern matrix.

    :param pattern_mtx: a matrix of integers representing the pattern
    :param fixed: True if all rows of the matrix are of equal length; is rectangular
    :return: the horizontally flipped pattern

    >>> photon = [[1, 0, 0], [0, 0, 1], [0, 0, 1], [1, 0, 0]]
    >>> flip_horizontal_pattern(photon)
    [[0, 0, 1], [1, 0, 0], [1, 0, 0], [0, 0, 1]]
    """
    if not fixed:
        pattern_mtx = fix_pattern(pattern_mtx)
    new_pattern = [row[::-1] for row in pattern_mtx]
    return new_pattern


def flip_vertical_pattern(pattern_mtx, fixed=True):
    """(list matrix of int[, bool]) -> list matrix of int

    Vertically flips the pattern matrix.

    :param pattern_mtx: a matrix of integers representing the pattern
    :param fixed: True if all rows of the matrix are of equal length; is rectangular
    :return: the vertically flipped pattern

    >>> glider = [[0, 1, 0], [0, 0, 1], [1, 1, 1]]
    >>> flip_vertical_pattern(glider)
    [[1, 1, 1], [0, 0, 1], [0, 1, 0]]
    """
    if not fixed:
        pattern_mtx = fix_pattern(pattern_mtx)
    return pattern_mtx[::-1]


def print_pattern(pattern_mtx: [[int]]) -> None:
    """(list matrix of int) -> NoneType

    Prints the pattern matrix.

    :param pattern_mtx: a matrix of integers representing the pattern

    >>> glider = [[0, 1, 0], [0, 0, 1], [1, 1, 1]]
    >>> print_pattern(glider)
    . o .
    . . o
    o o o
    >>> photon = [[1, 0, 0], [0, 0, 1], [0, 0, 1], [1, 0, 0]]
    >>> print_pattern(photon)
    o . .
    . . o
    . . o
    o . .
    """
    for cell_list in pattern_mtx:
        str_list = ['o' if cell == 1 else '.' for cell in cell_list]
        print(" ".join(str_list))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
