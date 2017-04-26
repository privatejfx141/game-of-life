import sys
import pygame as pg
from time import sleep
from game_of_life import *
from patterns import *

pg.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
LIGHTGREY = (223, 223, 223)
WHITE = (255, 255, 255)
TILESIZE = 5
SPEED = 0.06
FONT = pg.font.Font("FreeSansBold.ttf", 12)


def play(grid):
    """(list of list) -> NoneType

    Run the Game of Life.
    """
    # Get the number of rows and columns of the board.
    num_rows, num_cols = grid.dimensions()
    
    # Initialize the display surface.
    DISPLAY = pg.display.set_mode((num_cols*TILESIZE, num_rows*TILESIZE+40))
    pg.display.set_caption("Game of Life")

    RUNNING, PAUSE = 0, 1
    state = RUNNING
    run = True

    rule = grid.get_rule()
    generation = 0
    population = 0

    # Main game loop.
    while run:

        click = False
        remove_cell = False
        show_pause_text = False

        # Get the events.
        for event in pg.event.get():

            # If user wants to quit.
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.KEYDOWN:
                
                # If user presses space bar.
                if event.key == pg.K_SPACE and state == RUNNING:
                    show_pause_text = True
                    state = PAUSE
                
                # If user presses any other keys.
                else:
                    state = RUNNING
            
            if event.type == pg.MOUSEBUTTONDOWN:
                click = True

        if click:
            x, y = pg.mouse.get_pos()
            mouse_r, mouse_c = y // TILESIZE, x // TILESIZE
            if (mouse_r, mouse_c) in grid.alive_cells(by_value=False):
                remove_cell = True
            else:
                grid.add_cell(mouse_r, mouse_c)
            generation = 0
            population += 1

        if remove_cell:
            grid.alive_cells(by_value=False).remove((mouse_r, mouse_c))

        # If display is running.
        if state == RUNNING:

            # Colour the display background.
            DISPLAY.fill(GREY, (0, 0, num_cols * TILESIZE, 
                                num_rows * TILESIZE))
            DISPLAY.fill(BLACK, (0, num_rows * TILESIZE, num_cols * TILESIZE,
                                 num_rows * TILESIZE + 40))

            # Rate of display.
            sleep(SPEED)

            # Display text on bottom portion of display..
            text = FONT.render('Generation: ' + str(generation), True, WHITE)
            DISPLAY.blit(text, (10, num_rows * TILESIZE + 10))
            text = FONT.render('Population: ' + str(population), True, WHITE)
            DISPLAY.blit(text, (110, num_rows * TILESIZE + 10))
            text = FONT.render('Rule: ' + rule, True, WHITE)
            DISPLAY.blit(text, (210, num_rows * TILESIZE + 10))

            # Display the living cells as white squares.
            alive_cells = grid.alive_cells(by_value=False)
            for cell in alive_cells:
                pg.draw.rect(DISPLAY, WHITE,
                             (cell[1] * TILESIZE, cell[0] * TILESIZE,
                              TILESIZE, TILESIZE))
            # Step forward to the next generation on the board.
            grid.step()
            
            # Update the display surface.
            pg.display.update()

            # Increment to next generation.
            generation += 1
            population = len(alive_cells)

        # If display is paused.
        elif state == PAUSE:
            text = FONT.render('Paused', True, WHITE)

            if show_pause_text or click:
                if click:
                    if remove_cell:
                        colour = GREY
                    else:
                        colour = WHITE
                    pg.draw.rect(DISPLAY, colour,
                                 (mouse_c * TILESIZE, mouse_r * TILESIZE,
                                  TILESIZE, TILESIZE))
                if show_pause_text:
                    DISPLAY.blit(text, (300, num_rows * TILESIZE + 10))
                pg.display.update()
            pass

    # Exit the display.
    pg.quit()
    sys.exit()


if __name__ == '__main__':
    life = Grid(100, 100)
    life.add_pattern(COMMON['block'])
    play(life)
