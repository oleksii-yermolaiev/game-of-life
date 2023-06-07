# Sterowanie:
# LPM    - ustaw żywą komórkę
# PPM    - ustaw martwą komórkę
# escape - zmień reguły
# spacja - zatrzymaj, kontynuuj
# enter  - (kiedy zatrzymano) zrób jeden krok


import pygame as pg

from game import World


WIN_SIZE = (512, 512)
GRID_SIZE = (32, 32)
CELL_SIZE = (WIN_SIZE[0] / GRID_SIZE[0], WIN_SIZE[1] / GRID_SIZE[1])

STEP_TIME = 100

BACKGROUND_COLOR = (230, 230, 230)
GRID_COLOR = (120, 120, 120)
CELL_COLOR = (80, 80, 80)
HOVERED_CELL_COLOR = (180, 180, 180)


def draw_grid(screen):
    for x in range(GRID_SIZE[0]):
        pg.draw.line(
            screen,
            GRID_COLOR,
            (x * CELL_SIZE[0], 0),
            (x * CELL_SIZE[0], WIN_SIZE[1])
        )

    for y in range(GRID_SIZE[0]):
        pg.draw.line(
            screen,
            GRID_COLOR,
            (0, y * CELL_SIZE[1]),
            (WIN_SIZE[0], y * CELL_SIZE[1])
        )


def draw_cell(screen, pos, color):
    pg.draw.rect(
        screen,
        color,
        pg.Rect(
            pos[0] * CELL_SIZE[0],
            pos[1] * CELL_SIZE[1],
            CELL_SIZE[0],
            CELL_SIZE[1],
        )
    )


def draw_cells(screen, world):
    for pos in alive_cells(world):
        draw_cell(screen, pos, CELL_COLOR)


def screen_coords_to_world(pos):
    return int(pos[0] // CELL_SIZE[0]), \
           int(pos[1] // CELL_SIZE[1])


def update_title(paused, rule):
    paused_str = "Paused" if paused else "Running"
    rule_str = ''.join(map(str, rule[0])) + '/' + ''.join(map(str, rule[1]))
    pg.display.set_caption(f"Game of Life | {paused_str} | Rule: {rule_str}")


def parse_rule(string):
    split = string.split('/')
    return list(map(
        lambda chars: list(map(int, chars)),
        split
    ))


def main():
    paused = True
    rule = [
        [2, 3],
        [3],
    ]

    world = World(GRID_SIZE)
    
    screen = pg.display.set_mode((512, 512))
    pg.time.set_timer(pg.USEREVENT + 1, STEP_TIME)
    update_title(paused, rule)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    paused = not paused
                    update_title(paused, rule)

                elif event.key == pg.K_RETURN and paused:
                    step(world, rule)

                elif event.key == pg.K_ESCAPE:
                    rule = parse_rule(input("Enter new rule: "))
                    update_title(paused, rule)

            elif event.type == pg.USEREVENT + 1 and not paused:
                world.step(rule)

        hovered_pos = screen_coords_to_world(pg.mouse.get_pos())
        if pg.mouse.get_pressed()[0]:
            world.grid[hovered_pos[0]][hovered_pos[1]] = 1
        elif pg.mouse.get_pressed()[2]:
            world.grid[hovered_pos[0]][hovered_pos[1]] = 0

        screen.fill(BACKGROUND_COLOR)
        draw_cell(screen, hovered_pos, HOVERED_CELL_COLOR)
        draw_grid(screen)
        draw_cells(screen, world.grid)

        pg.display.flip()


if __name__ == "__main__":
    main()
