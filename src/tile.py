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

        self.health = spec.get('health') or 1

        self.sprite = spec['sprite'] if 'sprite' in spec else name
        if len(kind) > 0:
            self.sprite += '_' + kind
        
        self.buyable = 'buyable' in spec
        if self.buyable:
            self.price = spec['buyable'].get('price') or 0
            self.buy_entity = spec['buyable']['entity']

    def draw(self, screen, sprites, x, y) -> None:
        size = self.size
        sprites['field_grassy'].draw(screen, (x * size, y * size), (size, size))

        sprite = self.sprite
        if (self.burning):
            sprite += '_burning'
        sprites[sprite].draw(screen, (x * size, y * size), (size, size))

        if self.buyable:
            sprites['buyable'].draw(screen, (x * size, y * size), (size, size))
    
    def click(self) -> str | None:
        print(f"i'm a {self.sprite}")
        if self.buyable:
            return self.sprite
        return None

    def ignite(self):
        if self.flammable:
            self.burning = True

    def extinguish(self):
        self.burning = False