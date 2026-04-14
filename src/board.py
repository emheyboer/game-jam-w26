import json
import random

from tile import Tile

class Board:
    def __init__(self, width: int, height: int,
                 tiles: list[list[Tile]] | None = None) -> None:
        self.width = width
        self.height = height
        if tiles is None:
            tiles = [[Tile((x, y)) for y in range(0, height)] for x in range(0, width)]
        self.tiles: list[list[Tile]] = tiles
        self.wind_direction = (1, 0)

    def load_json(self, path):
        with open(path) as file:
            board = json.load(file)
        for region in board:
            for x in range(region['cols'][0], region['cols'][1] + 1):
                for y in range(region['rows'][0], region['rows'][1] + 1):
                    kind = region['kind'] if 'kind' in region else ''
                    burning = 'burning' in region and region['burning']
                    self.tiles[x][y] = Tile((x, y), region['name'], kind, burning)

    def draw(self, screen, sprites) -> None:
        for x in range(0, self.width):
            for y in range(0, self.height):
                tile = self.tiles[x][y]
                tile.draw(screen, sprites)

    def tick(self) -> None:
        if random.randint(1, 60 * 10) == 1:
            dir = (random.randint(-1, 1), random.randint(-1, 1))
            if dir == (0, 0):
                dir = (1, 1)
            self.wind_direction = dir

        for x in range(0, self.width):
            for y in range(0, self.height):
                tile = self.tiles[x][y]
                tile.tick(self)

    def find(self, pos, callback, max_radius: int = 100):
        """
        Searches the grid in an expanding square centered on the entity.
        Returns the first tile for which `callback` returns a truthy value
        """
        (x, y) = pos
        radius = 0
        while radius <= min(max(self.width, self.height), max_radius):
            tiles = []
            for t_x in range(x - radius, x + radius + 1):
                tiles.append((t_x, y + radius))
                tiles.append((t_x, y - radius))
            for t_y in range(y - radius + 1, y + radius):
                tiles.append((x + radius, t_y))
                tiles.append((x - radius, t_y))

            random.shuffle(tiles)
            for (t_x, t_y) in tiles:
                # potentially adding a bunch of junk coordinates just to
                # remove them here is of course a questionable approach
                if not (0 <= t_x < self.width) or not (0 <= t_y < self.height):
                    continue
                tile = self.tiles[t_x][t_y]
                if callback(tile):
                    return tile
            radius += 1