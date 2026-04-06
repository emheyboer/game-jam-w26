import json
import random

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
        
        tile = board.tiles[x][y]
        if tile.burning:
            tile.extinguish() 
        elif self.follow_flag and self.flag is None:
            self.find_flag(board)
        elif self.motile:
            self.move(board)

    def find_flag(self, board):
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
                if not (0 <= t_x < board.width) or not (0 <= t_y < board.height):
                    continue
                entity = board.tiles[t_x][t_y].entity
                if entity is not None and entity.is_flag:
                    self.flag = entity
                    return
            radius += 1

    def move(self, board):
        (x, y) = self.pos
        tile = board.tiles[x][y]

        (dx, dy) = (0, 0)
        if self.follow_flag and self.flag is not None:
            (flag_x, flag_y) = self.flag.pos
            # don't worry, i hate this too
            dx = (flag_x - x) // max(abs(flag_x - x), 1)
            dx = min(max(dx + random.randint(-1, 1), -1), 1)
            dy = (flag_y - y) // max(abs(flag_y - y), 1)
            dy = min(max(dy + random.randint(-1, 1), -1), 1)
        else:
            (dx, dy) = (random.randint(-1, 1), random.randint(-1, 1))
        
        (x, y) = (x + dx, y + dy)

        if not (0 <= x < board.width) or not (0 <= y < board.height):
            return
        
        new_tile = board.tiles[x][y]
        if new_tile.entity is not None:
            return
        
        tile.entity = None
        new_tile.entity = self
        self.pos = (x, y)