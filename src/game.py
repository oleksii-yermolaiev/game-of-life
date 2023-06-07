class World:
    # Tworzy pusty świat o rozmiarze size[0] x size[1].
    def __init__(self, size):
        self.size = size
        self.grid = [[0 for y in range(size[1])]
                     for x in range(size[0])]

    # Wykonuje 1 krok symulacji.
    # rule[0] - lista liczb sąsiadów, dla których żywa komórka zostaje żywą;
    # rule[1] - litsa liczb sąsiadów, dla któych martwa komórka zostaje żywą;
    # Inaczej komórka zostaje martwą.
    def step(self, rule):
        neighbor_counts = self.get_neighbor_counts()
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                cell_state = self.grid[x][y]
                becomes_alive = neighbor_counts[x][y] in rule[1 - cell_state]
                self.grid[x][y] = int(becomes_alive)

    # Zwraca siatkę z liczbą żywych sąsiadów dla każdej komórki.
    def get_neighbor_counts(self):
        result = [[0 for y in range(self.size[1])] for x in range(self.size[0])]
        for pos in self.alive_cells():
            for neighbor_pos in self.neighbors(pos):
                result[neighbor_pos[0]][neighbor_pos[1]] += 1

        return result

    # Generator zwracający współrzędne każdej żywej komórki.
    def alive_cells(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if self.grid[x][y]:
                    yield x, y


    # Generator zwracający współrzędne sąsiadów komórki.
    def neighbors(self, pos):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx or dy:
                    yield (pos[0] + dx) % self.size[0], \
                          (pos[1] + dy) % self.size[1]
