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

        self.ranged = spec.get('ranged') or False
        self.splash = spec.get('splash') or False
        self.self_refill = spec.get('self_refill') or False
        self.large_reservoir = spec.get('large_reservoir') or False

        self.follow_flag = spec.get('follow_flag') or False
        self.flag = None
        self.is_flag = spec.get('is_flag') or False

        self.is_alive = True

        self.pos = pos
        self.state = State.IDLE

    def draw(self, screen, sprites) -> None:
        size = self.size
        (x, y) = self.pos
        sprites[self.sprite].draw(screen, (x * size, y * size), (size, size))

        if self.state == State.REFILL:
            sprites[f"droplet_full"].draw(screen, (x * size, y * size), (size, size))

    def tick(self, board) -> None:
        if self.wait > 0:
            self.wait -= 1
            return
        self.wait = self.cooldown

        (x, y) = self.pos

        # our flag has been removed, so let's find another
        if self.flag is not None and not self.flag.is_alive:
            self.flag = None
            self.state = State.IDLE

        if self.follow_flag and self.flag is None:
            self.find_flag(board)
            if self.flag is not None:
                self.state = State.MOVE_TO_FLAG

        if self.state == State.IDLE and not self.follow_flag:
            self.state = State.EXTINGUISH

        if self.state == State.IDLE and self.motile:
            self.random_move(board)

        if self.state == State.MOVE_TO_FLAG and self.flag and self.motile:
            distance = self.distance_from_pos(self.flag.pos)
            if distance > 2:
                self.move_towards_pos(board, self.flag.pos)
            else:
                self.state = State.EXTINGUISH
            
        if self.state == State.EXTINGUISH and self.motile:
            tile = board.find(self.pos, lambda tile : tile.burning)
            if tile is not None:
                self.move_towards_pos(board, tile.pos)

        if self.state == State.REFILL:
            tile = board.tiles[x][y]
            can_fill = tile.water_source or self.self_refill
            if can_fill and self.follow_flag and self.flag:
                self.state = State.MOVE_TO_FLAG
            elif can_fill and self.follow_flag:
                self.state = State.IDLE
            elif can_fill:
                self.state = State.EXTINGUISH
        
        if self.state == State.REFILL and self.motile:
            tile = board.find(self.pos, lambda tile : tile.water_source)
            if tile is not None:
                self.move_towards_pos(board, tile.pos)

        # units don't have to be in the EXTINGUISH state
        # to actually extinguish a fire (since it'd be weird otherwise)
        tile = board.find(self.pos, lambda t : t.burning, 1 if self.ranged else 0)
        if self.state != State.REFILL and tile is not None and tile.burning:
            tile.extinguish()
            if self.splash:
                self.splash_extinguish(board, tile.pos)
            if not self.large_reservoir or random.randint(1, 4) == 1:
                self.state = State.REFILL

    def splash_extinguish(self, board, pos):
        (x, y) = pos
        targets = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]
        for (dx, dy) in targets:
            (t_x, t_y) = (x + dx, y + dy)
            if not (0 <= t_x < board.width) or not (0 <= t_y < board.height):
                continue
            board.tiles[t_x][t_y].extinguish()

    def find_flag(self, board):
        tile = board.find(self.pos,
                         lambda tile : tile.entity and tile.entity.is_flag)
        if tile is not None:
            self.flag = tile.entity

    def distance_from_pos(self, pos):
        (t_x, t_y) = pos
        (x, y) = self.pos
        return math.sqrt((t_x - x)**2 + (t_y - y)**2)

    def move_towards_pos(self, board, pos):
        (x, y) = self.pos
        (t_x, t_y) = pos

        # don't worry, i hate this too
        dx = (t_x - x) // max(abs(t_x- x), 1)
        dy = (t_y - y) // max(abs(t_y - y), 1)

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
            new_tile = board.find(new_tile.entity.pos, lambda t: t.entity is None, 1)
            if new_tile is None:
                return
            (x, y) = new_tile.pos
        
        tile.entity = None
        new_tile.entity = self
        self.pos = (x, y)

    def kill(self) -> None:
        self.is_alive = False