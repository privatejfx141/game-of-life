import sys
import pygame as pg
from game_of_life import *
from patterns import *
pg.init()

BLACK = (0, 0, 0)
CHARCOAL = (25, 25, 25)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
BLUE = (0, 0, 200)
CELLSIZE = 3
FPS = 20

FONT = pg.font.Font("FreeSansBold.ttf", 12)
    

def play(grid):
    """(Grid) -> NoneType
    
    Run the Game of Life.
    """
    # Get the dimensions of the grid and board.
    num_rows, num_cols = grid.dimensions()
    
    # Initialize display surface and Clock object.
    pg.display.set_caption("Game of Life")
    display = pg.display.set_mode((num_cols*CELLSIZE, num_rows*CELLSIZE+40))
    clock = pg.time.Clock()
    
    # Info to show on display surface.
    rule = grid.get_rule()
    generation = 0
    population = 0
    paused = True

    # Main game loop.
    while True:        

        # Set automaton fps.
        clock.tick(FPS)

        # Get the set of alive cells on the grid.
        alive_cells = grid.alive_cells(by_value=False)

        # Get mouse position.
        x, y = pg.mouse.get_pos()
        mouseX, mouseY = x // CELLSIZE, y // CELLSIZE

        # Get user events.
        for event in pg.event.get():

            # If user exits the program.
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # If user presses on a key.
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    paused = not paused

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

        # Fill the display surface background colours.
        display.fill(GREY, (0, 0, num_cols * CELLSIZE, num_rows * CELLSIZE))
        display.fill(CHARCOAL, (0, num_rows * CELLSIZE, num_cols * CELLSIZE, num_rows * CELLSIZE + 80))
        # Display the cells.
        for cell in alive_cells:
            pg.draw.rect(display, WHITE, (cell[1] * CELLSIZE, cell[0] * CELLSIZE, CELLSIZE, CELLSIZE))
        population = len(alive_cells)
        # Highlight whatever cell the mouse is hovering upon.
        if mouseY < num_rows:
            pg.draw.rect(display, BLUE, (mouseX * CELLSIZE, mouseY * CELLSIZE, CELLSIZE, CELLSIZE), 1)
        # Display game rule.
        text = FONT.render('Rule: ' + rule, True, WHITE)
        display.blit(text, (250, num_rows * CELLSIZE + 10))
        # Display generation count.
        text = FONT.render('Generation: ' + str(generation), True, WHITE)
        display.blit(text, (10, num_rows * CELLSIZE + 10))
        # Display population count.
        text = FONT.render('Population: ' + str(population), True, WHITE)
        display.blit(text, (130, num_rows * CELLSIZE + 10))

        # If automaton is paused.
        if paused:
            # Display 'Paused' on bottom-right corner.
            display.blit(FONT.render('Paused', True, WHITE), (
                num_cols * CELLSIZE - 60, num_rows * CELLSIZE + 10))
        # If automaton is running.
        else:
            # Step forward to the next generation on the grid.
            grid.step()
            generation += 1

        # Update the display.
        pg.display.flip()


if __name__ == '__main__':
    life = Grid(200, 300)
    life.add_pattern(transpose_pattern(SPACESHIP['steamship']))
    play(life)
