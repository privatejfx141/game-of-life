from patterns import *


def create_board(rows, cols):
    """(int, int) -> list of list

    Create and return a boolean board of rows rows and cols columns.
    """
    return [[False]*cols for r in range(rows)]


def add_cell(board, r, c, value=True):
    """(list of list, int, int[, object]) -> NoneType

    Set cell at (r, c) with value to the board.
    """
    board[r % len(board)][c % len(board[0])] = value


def add_pattern(board, pattern, r, c):
    """(list of list, list of list, int, int) -> NoneType

    Add pattern to (r, c) on the board.
    """
    for h in range(len(pattern)):
        for w in range(len(pattern[0])):
            if pattern[h][w] == 1:
                board[(r + h) % len(board)][(c + w) % len(board[0])] = True


def pattern_to_board(pattern):
    """(list of list of int) -> list of list of bool

    Convert pattern to a life board.
    """
    board = list()
    for r in range(len(pattern)):
        board.append(list())
        for c in range(len(pattern[0])):
            board[r].append(True if pattern[r][c] == 1 else False)
    return board


def neighbours(board, r, c):
    """(list of list, int, int) -> int
    
    Return the number of alive neighbours around cell at (r, c).
    """
    count = 0
    for ver in [-1, 0, 1]:
        for hor in [-1, 0, 1]:
            if not (ver == hor == 0):
                # If neighbour is alive, increment counter.
                if board[(r+ver) % len(board)][(c+hor) % len(board[0])]:
                    count += 1
    return count


def step(board, count=1):
    """(list of list[, int]) -> list of list

    Play the simulation and return board at generation count.
    """
    # Get the number of rows and columns.
    num_rows, num_cols = len(board), len(board[0])
    # Create a copy of the board.
    curr_board = [row.copy() for row in board]

    # Loop through each generation.
    for generation in range(count):
        # Create an empty new board.
        new_board = create_board(num_rows, num_cols)
        # Loop through each cell.
        for r in range(num_rows):
            for c in range(num_cols):
                # Get number of neighbours of the current cell.
                nbs = neighbours(curr_board, r, c)
                # Determine which cell lives on to the next generation.
                was_alive = curr_board[r][c]
                is_alive = nbs == 3 or (nbs == 2 and was_alive)
                new_board[r][c] = is_alive
        # Set new board as current board.
        curr_board = new_board

    # Return the board at generation count.
    return curr_board


def alive_cells(board):
    """(list of list) -> set of {(int, int)}
    
    Return the set of coordinates of all alive cells.
    """
    alive = set()
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c]:
                alive.add((r, c))
    return alive


def draw_board(board):
    """(list of list) -> str

    Return the string representation of board.
    """
    res = ''
    # Return the number of rows and columns
    num_rows, num_cols = len(board), len(board[0])
    # Loop through each cell.
    for r in range(num_rows):
        for c in range(num_cols):
            res += 'o' if board[r][c] else '.'
            if c != num_cols-1:
                res += ' '
        if r != num_rows-1:
            res += '\n'
    # Return the string representation.
    return res


if __name__ == '__main__':
    life = create_board(10, 10)
    add_pattern(life, COMMON['glider'], 4, 4)
    print(draw_board(step(life, 2)))
