"""
Sterowanie:
LPM    - ustaw żywą komórkę
PPM    - ustaw martwą komórkę
escape - zmień reguły
spacja - zatrzymaj, kontynuuj
enter  - (kiedy zatrzymano) zrób jeden krok
"""


import pygame as pg

from game import World, WorldGraphics
from menu import Menu

WIN_SIZE = (512, 512)
GRID_SIZE = (32, 32)
CELL_SIZE = (WIN_SIZE[0] / GRID_SIZE[0], WIN_SIZE[1] / GRID_SIZE[1])

STEP_TIME = 100

BACKGROUND_COLOR = (230, 230, 230)
HOVERED_CELL_COLOR = (180, 180, 180)


def screen_coords_to_world(pos):
    return int(pos[0] // CELL_SIZE[0]), \
           int(pos[1] // CELL_SIZE[1])


def update_title(paused, rule):
    paused_str = "Paused" if paused else "Running"
    pg.display.set_caption(f"Game of Life | {paused_str}")


def main():
    paused = True
    menu = Menu(WIN_SIZE)

    world = World(GRID_SIZE)
    graphics = WorldGraphics(world, CELL_SIZE)
    
    screen = pg.display.set_mode((512, 512))
    pg.time.set_timer(pg.USEREVENT + 1, STEP_TIME)
    update_title(paused, menu.rule)

    while True:
        for event in pg.event.get():
            if menu.on_event(event):
                continue

            elif event.type == pg.QUIT:
                return

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    paused = not paused
                    update_title(paused, menu.rule)

                elif event.key == pg.K_RETURN and paused:
                    world.step(menu.rule)

                elif event.key == pg.K_ESCAPE:
                    rule = menu.get_rule()
                    update_title(paused, menu.rule)

            elif event.type == pg.USEREVENT + 1 and not paused:
                world.step(menu.rule)

        hovered_pos = screen_coords_to_world(pg.mouse.get_pos())
        if pg.mouse.get_pressed()[0]:
            world.grid[hovered_pos[0]][hovered_pos[1]] = 1
        elif pg.mouse.get_pressed()[2]:
            world.grid[hovered_pos[0]][hovered_pos[1]] = 0

        screen.fill(BACKGROUND_COLOR)
        graphics.draw_cell(screen, hovered_pos, HOVERED_CELL_COLOR)
        graphics.draw(screen)

        menu.draw(screen)

        pg.display.flip()


if __name__ == "__main__":
    main()
