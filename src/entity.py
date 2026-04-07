import json
import random
import math
from enum import Enum

class State(Enum):
    IDLE = 0
    MOVE_TO_FLAG = 1
    EXTINGUISH = 2
    REFILL = 3

def load_definitions(path):
    with open(path) as file:
        return json.load(file)

class Entity:
    size = 32
    definitions = load_definitions('src/entities.json')
    def __init__(self, pos: tuple[int, int], name: str = '') -> None:
        spec = self.definitions[name] if name in self.definitions else {}

        self.sprite = spec['sprite'] if 'sprite' in spec else name

        self.motile = spec.get('motile') or False
        self.cooldown = spec.get('cooldown') or 30
        self.wait = self.cooldown

        self.follow_flag = spec.get('follow_flag') or False
        self.flag = None
        self.is_flag = spec.get('is_flag') or False

        self.pos = pos
        self.state = State.IDLE

    def draw(self, screen, sprites) -> None:
        size = self.size
        (x, y) = self.pos
        sprites[self.sprite].draw(screen, (x * size, y * size), (size, size))

    def tick(self, board) -> None:
        if self.wait > 0:
            self.wait -= 1
            return
        self.wait = self.cooldown

        (x, y) = self.pos

        if self.follow_flag and self.flag is None:
            self.find_flag(board)
            if self.flag is not None:
                self.state = State.MOVE_TO_FLAG

        if self.state == State.IDLE and self.motile:
            self.random_move(board)

        if self.state == State.MOVE_TO_FLAG and self.flag and self.motile:
            distance = self.distance_from_flag()
            if distance > 2:
                self.move_towards_pos(board, self.flag.pos)
            else:
                self.state = State.EXTINGUISH
            
        if self.state == State.EXTINGUISH and self.motile:
            tile = self.find(board, lambda tile : tile.burning)
            if tile is not None:
                self.move_towards_pos(board, tile.pos)

        tile = board.tiles[x][y]
        if tile.burning:
            tile.extinguish()
            if self.follow_flag and self.flag:
                self.state = State.MOVE_TO_FLAG


    def find(self, board, callback):
        """
        Searches the grid in an expanding square centered on the entity.
        Returns the first tile for which `callback` returns a truthy value
        """
        (x, y) = self.pos
        radius = 1
        while radius <= max(board.width, board.height):
            tiles = []
            for t_x in range(x - radius, x + radius + 1):
                tiles.append((t_x, y + radius))
                tiles.append((t_x, y - radius))
            for t_y in range(y - radius + 1, y + radius):
                tiles.append((x + radius, t_y))
                tiles.append((x - radius, t_y))

            for (t_x, t_y) in tiles:
                # potentially adding a bunch of junk coordinates just to
                # remove them here is of course a questionable approach
                if not (0 <= t_x < board.width) or not (0 <= t_y < board.height):
                    continue
                tile = board.tiles[t_x][t_y]
                if callback(tile):
                    return tile
            radius += 1

    def find_flag(self, board):
        tile = self.find(board,
                         lambda tile : tile.entity and tile.entity.is_flag)
        if tile is not None:
            self.flag = tile.entity

    def distance_from_flag(self):
        if self.flag is None:
            return -1
        (flag_x, flag_y) = self.flag.pos
        (x, y) = self.pos
        return math.sqrt((flag_x - x)**2 + (flag_y - y)**2)

    def move_towards_pos(self, board, pos):
        (x, y) = self.pos
        (t_x, t_y) = pos
        # don't worry, i hate this too
        dx = (t_x - x) // max(abs(t_x- x), 1)
        dx = min(max(dx + random.randint(-1, 1), -1), 1)
        dy = (t_y - y) // max(abs(t_y - y), 1)
        dy = min(max(dy + random.randint(-1, 1), -1), 1)

        self.move(board, (dx, dy))

    def random_move(self, board):
        (dx, dy) = (random.randint(-1, 1), random.randint(-1, 1))
        self.move(board, (dx, dy))

    def move(self, board, dir):
        (dx, dy) = dir
        (x, y) = self.pos
        tile = board.tiles[x][y]
        
        (x, y) = (x + dx, y + dy)

        if not (0 <= x < board.width) or not (0 <= y < board.height):
            return
        
        new_tile = board.tiles[x][y]
        if new_tile.entity is not None:
            return
        
        tile.entity = None
        new_tile.entity = self
        self.pos = (x, y)