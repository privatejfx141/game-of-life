"""
KEYBOARD CONTROLS:

SPACE       pause/resume the simulation
RETURN      step to the next generation (req. pause)
q           exit the program
a           revert back to initial state
s           clear the grid of alive cells
f           display/hide GPS rate
g           display grid lines
,           decrease GPS rate
.           increase GPS rate
"""

import sys
import pygame as pg
from game_of_life import *
from colours import *
from patterns import *
pg.init()

CELLSIZE = 6
ICON = pg.image.load("gol_glider.png")
pg.display.set_icon(ICON)
FONT = pg.font.Font("FreeSansBold.ttf", 12)
    

def terminate():
    pg.quit()
    sys.exit()


def play(grid):
    """(Grid) -> NoneType
    
    Run the Game of Life.
    """
    # Get original configuration.
    original_cells = grid.alive_cells(by_value=True)

    # Get the dimensions of the grid and board.
    num_rows, num_cols = grid.dimensions()
    
    # Initialize display surface and Clock object.
    pg.display.set_caption("Game of Life")
    display = pg.display.set_mode((num_cols*CELLSIZE, num_rows*CELLSIZE+40))
    clock = pg.time.Clock()
    
    # Info to show on display surface.
    rule = grid.get_rule()
    generation = 0
    population = len(original_cells)
    paused = True
    gps = 100
    show_grid_lines = False
    show_gps = False

    # Colour choice
    bg_colour = 0
    cell_colour = 0

    # Main game loop.
    while True:

        manual_step = False

        # Set automaton fps.
        clock.tick(gps)

        # Get the set of alive cells on the grid.
        alive_cells = grid.alive_cells(by_value=False)

        # Get mouse position.
        x, y = pg.mouse.get_pos()
        mouseX, mouseY = x // CELLSIZE, y // CELLSIZE

        # If one of the arrow keys is pressed.
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] or keys[pg.K_DOWN]\
                or keys[pg.K_LEFT] or keys[pg.K_RIGHT]:
            moved_cells = set()
            r_add, c_add = 0, 0
            if keys[pg.K_UP]:
                r_add = 1
            if keys[pg.K_DOWN]:
                r_add = -1
            if keys[pg.K_LEFT]:
                c_add = 1
            if keys[pg.K_RIGHT]:
                c_add = -1
            for cell in alive_cells:
                moved_cells.add(
                    ((cell[0]+r_add) % num_rows, (cell[1]+c_add) % num_cols))
            grid.set_cells(*moved_cells)
        # Get user events.
        for event in pg.event.get():

            # If user exits the program.
            if event.type == pg.QUIT:
                terminate()

            # If user presses on a key.
            if event.type == pg.KEYDOWN:
                print(event.key)
                # If space key, pause/resume simulation.
                if event.key == pg.K_SPACE:
                    paused = not paused
                # If enter key, step to next generation.
                if event.key == pg.K_RETURN:
                    manual_step = True
                # If c key, clear grid of alive cells.
                if event.key == pg.K_s:
                    grid.clear()
                    paused = True
                    generation = 0
                    population = 0
                # If g key, display/hide grid lines.
                if event.key == pg.K_g:
                    show_grid_lines = not show_grid_lines
                # If r key, revert back to initial state as inputted.
                if event.key == pg.K_a:
                    grid.set_cells(*original_cells)
                    paused = True
                    generation = 0
                    population = len(original_cells)
                if event.key == pg.K_f:
                    show_gps = not show_gps

                if event.key == pg.K_n:
                    bg_colour = (bg_colour + 1) % len(BG_COLOURS)

                if event.key == pg.K_m:
                    cell_colour = (cell_colour + 1) % len(CELL_COLOURS)

                # If q key, exit the program.
                if event.key == pg.K_q:
                    terminate()
                # If period or comma, increase/decrease GPS rate.
                if event.key == pg.K_PERIOD and gps < 50:
                    gps += 1
                elif event.key == pg.K_COMMA and gps > 1:
                    gps -= 1

            # If user left clicks somewhere on the grid.
            if event.type == pg.MOUSEBUTTONDOWN and mouseY < num_rows:
                # If cell is alive, kill it.
                if (mouseY, mouseX) in alive_cells:
                    alive_cells.remove((mouseY, mouseX))
                    population -= 1
                # If cell is dead, revive it.
                else:
                    grid.add_cell(mouseY, mouseX)
                    population += 1
                # Manual modification resets generation counter.
                generation = 0

        # Fill the grid background colour.
        display.fill(BG_COLOURS[bg_colour], (
            0, 0, num_cols * CELLSIZE, num_rows * CELLSIZE))
        # Fill the footer background colour.
        display.fill(RAISIN, (
            0, num_rows * CELLSIZE, num_cols * CELLSIZE, num_rows * CELLSIZE + 80))
        # Display the cells.
        for cell in alive_cells:
            pg.draw.rect(display, CELL_COLOURS[cell_colour], (
                cell[1] * CELLSIZE, cell[0] * CELLSIZE, CELLSIZE, CELLSIZE))
        population = len(alive_cells)
        # Display grid lines.
        if show_grid_lines:
            add = 0
            for i in range(max(num_rows, num_cols)):
                pg.draw.line(display, CHARCOAL, (
                    0, CELLSIZE + add), (CELLSIZE * num_cols, CELLSIZE + add))
                pg.draw.line(display, CHARCOAL, (
                    CELLSIZE + add, 0), (CELLSIZE + add, CELLSIZE * num_rows))
                add += CELLSIZE
        # Highlight whatever cell the mouse is hovering upon.
        if mouseY < num_rows:
            pg.draw.rect(display, SPACE_CADET, (
                mouseX * CELLSIZE, mouseY * CELLSIZE, CELLSIZE, CELLSIZE), 1)
        # Display game rule.
        text = FONT.render('Rule: ' + rule, True, WHITE)
        display.blit(text, (250, num_rows * CELLSIZE + 10))
        # Display generation count.
        text = FONT.render('Generation: ' + str(generation), True, WHITE)
        display.blit(text, (10, num_rows * CELLSIZE + 10))
        # Display population count.
        text = FONT.render('Population: ' + str(population), True, WHITE)
        display.blit(text, (130, num_rows * CELLSIZE + 10))
        # Display GPS rate.
        if show_gps:
            text = FONT.render('GPS: {}'.format(gps), True, CHARCOAL)
            display.blit(text, (2, 2))

        # If simulation is paused.
        if paused:
            # Display 'Paused' on bottom-right corner.
            display.blit(FONT.render('Paused', True, WHITE), (
                num_cols * CELLSIZE - 60, num_rows * CELLSIZE + 10))
        # If simulation is running.
        if not paused or manual_step:
            # Step forward to the next generation on the grid.
            grid.step()
            generation += 1

        # Update the display.
        pg.display.flip()


if __name__ == '__main__':
    life = Grid(100, 200)
    life.add_pattern(transpose_pattern(SPACESHIP['glider']))
    play(life)
