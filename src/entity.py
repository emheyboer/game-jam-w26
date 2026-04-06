import json
import random

def load_definitions(path):
    with open(path) as file:
        return json.load(file)

class Entity:
    size = 32
    definitions = load_definitions('src/entities.json')
    def __init__(self, name: str = '') -> None:
        spec = self.definitions[name] if name in self.definitions else {}

        self.sprite = spec['sprite'] if 'sprite' in spec else name

        self.motile = spec.get('motile') or False
        self.cooldown = spec.get('cooldown') or 60
        self.wait = self.cooldown

    def draw(self, screen, sprites, x, y) -> None:
        size = self.size
        sprites[self.sprite].draw(screen, (x * size, y * size), (size, size))

    def tick(self, board, x, y) -> None:
        if self.wait > 0:
            self.wait -= 1
            return
        self.wait = self.cooldown
        
        tile = board.tiles[x][y]
        if tile.burning:
            tile.extinguish()   
        elif self.motile:
            self.move(board, x, y)
    
    def move(self, board, x, y):
        tile = board.tiles[x][y]

        (dx, dy) = (random.randint(-1, 1), random.randint(-1, 1))
        (x, y) = (x + dx, y + dy)

        if not (0 < x < board.width) or not (0 < y < board.height):
            return
        
        new_tile = board.tiles[x][y]
        if new_tile.entity is not None:
            return
        
        tile.entity = None
        new_tile.entity = self