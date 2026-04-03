import json

from tile import Tile

class Board:
    def __init__(self, width: int, height: int,
                 tiles: list[list[Tile]] | None = None) -> None:
        self.width = width
        self.height = height
        if tiles is None:
            tiles = [[Tile() for _ in range(0, height)] for _ in range(0, width)]
        self.tiles: list[list[Tile]] = tiles

    def load_json(self, path):
        with open(path) as file:
            board = json.load(file)
        for region in board:
            for x in range(region['cols'][0], region['cols'][1] + 1):
                for y in range(region['rows'][0], region['rows'][1] + 1):
                    kind = region['kind'] if 'kind' in region else ''
                    burning = 'burning' in region and region['burning']
                    self.tiles[x][y] = Tile(region['name'], kind, burning)

    def draw(self, screen, sprites):
        for x in range(0, self.width):
            for y in range(0, self.height):
                tile = self.tiles[x][y]
                tile.draw(screen, sprites, x, y)