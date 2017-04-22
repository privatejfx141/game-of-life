import sys
import pygame as pg
from time import sleep
from game_of_life import *
from patterns import *

pg.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
TILESIZE = 4
FONT = pg.font.Font("FreeSansBold.ttf", 18)


def play(board):
    """(list of list) -> NoneType

    Run the Game of Life.
    """
    # Get the number of rows and columns of the board.
    num_rows, num_cols = len(board), len(board[0])
    
    # Initialize the display surface.
    DISPLAY = pg.display.set_mode((num_cols*TILESIZE, num_rows*TILESIZE+50))
    pg.display.set_caption("Game of Life")

    RUNNING, PAUSE = 0, 1    
    state = RUNNING
    run = True

    generation = 0

    # Main game loop.
    while run:

        # Get the events.
        for event in pg.event.get():
            
            # If user wants to quit.
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.KEYDOWN:
                
                # If user presses space bar.
                if event.key == pg.K_SPACE:
                    state = PAUSE
                
                # If user presses any other keys.
                else:
                    state = RUNNING

        # If display is running.
        if state == RUNNING:

            # Colour the display background.
            DISPLAY.fill(GREY, (0, 0, num_cols * TILESIZE, 
                                num_rows * TILESIZE))
            DISPLAY.fill(BLACK, (0, num_rows * TILESIZE, num_cols * TILESIZE, 
                                 num_rows * TILESIZE + 50))

            # Rate of display.
            sleep(0.01)

            # Display text on bottom portion of display..
            text = FONT.render('Generation ' + str(generation), True, WHITE)
            DISPLAY.blit(text, (10, num_rows * TILESIZE + 10))

            # Display the living cells as white squares.
            for cell in alive_cells(board):
                pg.draw.rect(DISPLAY, WHITE,
                             (cell[1] * TILESIZE, cell[0] * TILESIZE,
                              TILESIZE, TILESIZE))
            # Step forward to the next generation on the board.
            board = step(board)
            
            
            
            # Update the display surface.
            pg.display.update()

            # Increment to next generation.
            generation += 1

        # If display is paused.
        elif state == PAUSE:
            pass

    # Exit the display.
    pg.quit()
    sys.exit()


if __name__ == '__main__':
    life = create_board(100, 100)
    add_pattern(life, COMMON['glider'], 0, 0)
    add_pattern(life, COMMON['glider'], 0, 10)
    add_pattern(life, COMMON['glider'], 0, 20)
    add_pattern(life, COMMON['glider'], 0, 30)
    add_pattern(life, COMMON['glider'], 0, 40)
    add_pattern(life, COMMON['glider'], 0, 50)
    add_pattern(life, COMMON['r-pentomino'], 10, 90)
    play(life)
