import pygame as pg


class World:
    def __init__(self, size):
        """Tworzy pusty świat o rozmiarze size[0] x size[1]."""
        self.size = size
        self.grid = [[0 for y in range(size[1])]
                     for x in range(size[0])]

    def step(self, rule):
        """Wykonuje 1 krok symulacji.
        rule[0][liczba sąsiadów] - nowy stan komórki, jeżeli żyje;
        rule[1][liczba sąsiadów] - nowy stan komórki, jeżeli nie żyje;
        Inaczej komórka zostaje martwą.
        """
        neighbor_counts = self.get_neighbor_counts()
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                cell_state = self.grid[x][y]
                becomes_alive = rule[1 - cell_state][neighbor_counts[x][y]]
                self.grid[x][y] = int(becomes_alive)

    def get_neighbor_counts(self):
        """Zwraca siatkę z liczbą żywych sąsiadów dla każdej komórki."""
        result = [
            [0 for y in range(self.size[1])]
            for x in range(self.size[0])
        ]
        for pos in self.alive_cells():
            for neighbor_pos in self.neighbors(pos):
                result[neighbor_pos[0]][neighbor_pos[1]] += 1

        return result

    def alive_cells(self):
        """Generator zwracający współrzędne każdej żywej komórki."""
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if self.grid[x][y]:
                    yield x, y

    def neighbors(self, pos):
        """Generator zwracający współrzędne sąsiadów komórki."""
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx or dy:
                    yield (pos[0] + dx) % self.size[0], \
                          (pos[1] + dy) % self.size[1]


class WorldGraphics:
    GRID_COLOR = (120, 120, 120)
    CELL_COLOR = (80, 80, 80)

    def __init__(self, world, cell_size):
        self.cell_size = cell_size
        self.world = world

    def draw(self, screen):
        """Rysuje cały świat i siatkę."""
        self.draw_grid(screen)
        self.draw_cells(screen)

    def draw_grid(self, screen):
        """Rysuje siatkę"""
        screen_size = screen.get_size()

        for x in range(self.world.size[0]):
            pg.draw.line(
                screen,
                WorldGraphics.GRID_COLOR,
                (x * self.cell_size[0], 0),
                (x * self.cell_size[0], screen_size[1])
            )

        for y in range(self.world.size[0]):
            pg.draw.line(
                screen,
                WorldGraphics.GRID_COLOR,
                (0, y * self.cell_size[1]),
                (screen_size[0], y * self.cell_size[1])
            )

    def draw_cells(self, screen):
        """Rysuje wszystkie żywe komórki."""
        for pos in self.world.alive_cells():
            self.draw_cell(screen, pos, WorldGraphics.CELL_COLOR)

    def draw_cell(self, screen, pos, color):
        """Rysuje jedną komórkę."""
        pg.draw.rect(
            screen,
            color,
            pg.Rect(
                pos[0] * self.cell_size[0],
                pos[1] * self.cell_size[1],
                self.cell_size[0],
                self.cell_size[1],
            )
        )
