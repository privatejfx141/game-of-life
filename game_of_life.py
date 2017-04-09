class Board(object):
    """List of list implementation of a torus 2D board."""

    def __init__(self, n_rows, n_cols, cell='0'):
        """(Board, int, int) -> NoneType

        Create a torus board with n_rows rows and n_cols columns.
        """
        self._b = [[cell] * n_cols for r in range(n_rows)]
        self.cell = cell
        self._rows = n_rows
        self._cols = n_cols

    def __str__(self):
        """(Board) -> NoneType"""
        res = ''
        for row in self._b:
            for c in row:
                res += str(c) + ' '
            res = res[:-1] + '\n'
        return res[:-1]

    def get_cell(self, r, c):
        """(Board, int, int) -> object

        Return the value of the cell at row r and column c.
        """
        return self._b[r % self._rows][c % self._cols]

    def set_cell(self, r, c, value):
        """(Board, int, int, object) -> NoneType

        Set the value of the cell at row r and column c.
        """
        self._b[r % self._rows][c % self._cols] = value

    def num_rows(self):
        """(Board) -> int

        Return the number of rows of this board.
        """
        return self._rows

    def num_cols(self):
        """(Board) -> int

        Return the number of columns of this board.
        """
        return self._cols


class LifeBoard(Board):
    """Torus board implementation of Conway's Game of Life."""

    a = '#'
    d = '.'

    def __init__(self, n_rows, n_cols):
        """(LifeBoard, int, int) -> NoneType"""
        Board.__init__(self, n_rows, n_cols, self.d)

    def _live_neighbours(self, r, c):
        """(LifeBoard, int, int) -> int"""
        nw = self.get_cell(r-1, c-1)
        nn = self.get_cell(r-1, c)
        ne = self.get_cell(r-1, c+1)
        ee = self.get_cell(r, c+1)
        se = self.get_cell(r+1, c+1)
        ss = self.get_cell(r+1, c)
        sw = self.get_cell(r+1, c-1)
        ww = self.get_cell(r, c-1)
        return (nw, nn, ne, ee, se, ss, sw, ww).count(self.a)

    def next_state(self):
        """(LifeBoard) -> LifeBoard"""
        new_b = LifeBoard(self._rows, self._cols)

        for r in range(self._rows):
            for c in range(self._cols):
                live_nbs = self._live_neighbours(r, c)
                if self.get_cell(r, c) == self.a:
                    if live_nbs in (2, 3):
                        new_b.set_cell(r, c, self.a)
                else:
                    if live_nbs == 3:
                        new_b.set_cell(r, c, self.a)
        return new_b

    def state_at_generation(self, generation):
        """(LifeBoard, int) -> LifeBoard"""
        board = self
        for gen in range(generation):
            board = board.next_state()
        return board

    def set_pattern(self, *coordinates):
        """(LifeBoard, tuple of tuple)"""
        for coord in coordinates:
            self.set_cell(*coord, self.a)

    @staticmethod
    def _calc_cds(r, c, *offsets):
        cds = list()
        for o in offsets:
            cds.append((o[0]+r, o[1]+c))
        return cds

    def add_block(self, r, c):
        offsets = (0, 0), (0, 1), (1, 0), (1, 1)
        self.set_pattern(*LifeBoard._calc_cds(r, c, *offsets))

    def add_blinker(self, r, c):
        offsets = [(0, -1+i) for i in range(3)]
        self.set_pattern(*LifeBoard._calc_cds(r, c, *offsets))

    def add_beacon(self, r, c):
        self.add_block(r-1, c-1)
        self.add_block(r+1, c+1)

    def add_clock(self, r, c):
        offsets = (0, -1), (-1, 1), (0, 1), (1, 2), (2, 0), (1, 0)
        self.set_pattern(*LifeBoard._calc_cds(r, c, *offsets))

    def add_r_pentomino(self, r, c):
        offsets = (0, 0), (-1, 0), (-1, 1), (0, -1), (1, 0)
        self.set_pattern(*LifeBoard._calc_cds(r, c, *offsets))

    def add_glider(self, r, c):
        offsets = (-1, 0), (0, 1), (1, -1), (1, 0), (1, 1)
        self.set_pattern(*LifeBoard._calc_cds(r, c, *offsets))

    def add_lwss(self, r, c):
        offsets = [(-1, -2), (-1, 1), (1, -2), (0, 2), (1, 2)]
        offsets += [(2, -1+i) for i in range(4)]
        self.set_pattern(*LifeBoard._calc_cds(r, c, *offsets))

    def add_pentadecathlon(self, r, c):
        offsets = [(0, -5+i) for i in range(10)]
        self.set_pattern(*LifeBoard._calc_cds(r, c, *offsets))


if __name__ == '__main__':
    gol = LifeBoard(10, 10)
    gol.add_glider(4, 4)
    print(gol)
