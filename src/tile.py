import json

def load_definitions(path):
    with open(path) as file:
        return json.load(file)

class Tile:
    size = 32
    definitions = load_definitions('src/tiles.json')
    def __init__(self, name: str = '', kind: str = '', burning = False) -> None:
        spec = self.definitions[name] if name in self.definitions else {}

        self.flammable = 'flammable' in spec and spec['flammable']
        self.burning: bool = burning
        self.health = spec['health'] if 'health' in spec else 1
        self.sprite = spec['sprite'] if 'sprite' in spec else name
        if len(kind) > 0:
            self.sprite += '_' + kind

    def draw(self, screen, sprites, x, y) -> None:
        size = self.size
        sprites['field_grassy'].draw(screen, (x * size, y * size), (size, size))

        sprite = self.sprite
        if (self.burning):
            sprite += '_burning'
        sprites[sprite].draw(screen, (x * size, y * size), (size, size))