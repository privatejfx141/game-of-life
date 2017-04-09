from game_of_life import LifeBoard

msgs = {0: "Welcome to my implementation of Conway's Game of Life.",
        1: "To begin, enter the number of rows and columns.",
        2: 'Enter the number of rows (5, 100): ',
        3: 'Enter the number of columns (5, 100): '}
menu = """
Available options:
HELP      Displays this menu.
NEW       Creates a new board.
EXIT      Exits this program.

ADD       Adds a pattern to this board.
  BLOCK
  GLIDER
  R-PENTOMINO
  LWSS
"""


def main():
    print(msgs[0])
    print(msgs[1])
    rows = int(input(msgs[2]))
    cols = int(input(msgs[3]))
    board = LifeBoard(rows, cols)
    print(board)

main()
