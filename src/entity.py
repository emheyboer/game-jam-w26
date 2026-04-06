import json

def load_definitions(path):
    with open(path) as file:
        return json.load(file)

class Entity:
    size = 32
    definitions = load_definitions('src/entities.json')
    def __init__(self, name: str = '') -> None:
        spec = self.definitions[name] if name in self.definitions else {}

        self.sprite = spec['sprite'] if 'sprite' in spec else name

    def draw(self, screen, sprites, x, y) -> None:
        size = self.size
        sprites[self.sprite].draw(screen, (x * size, y * size), (size, size))