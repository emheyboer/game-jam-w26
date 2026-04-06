import json

from entity import Entity

def load_definitions(path):
    with open(path) as file:
        return json.load(file)

class Tile:
    size = 32
    definitions = load_definitions('src/tiles.json')
    def __init__(self, name: str = '', kind: str = '', burning = False) -> None:
        spec: dict = self.definitions[name] if name in self.definitions else {}

        self.flammable: bool = 'flammable' in spec and spec['flammable']
        self.burning: bool = burning

        self.health: int = spec.get('health') or 1

        self.sprite: str = spec['sprite'] if 'sprite' in spec else name
        if len(kind) > 0:
            self.sprite += '_' + kind
        
        self.buyable: bool = 'buyable' in spec
        if self.buyable:
            self.price: int = spec['buyable'].get('price') or 0
            self.buy_entity: str = spec['buyable']['entity']

        self.entity: Entity | None = None

    def draw(self, screen, sprites, x, y) -> None:
        size = self.size
        sprites['field_grassy'].draw(screen, (x * size, y * size), (size, size))

        sprite = self.sprite
        if (self.burning):
            sprite += '_burning'
        sprites[sprite].draw(screen, (x * size, y * size), (size, size))

        if self.buyable:
            sprites['buyable'].draw(screen, (x * size, y * size), (size, size))

        if self.entity is not None:
            self.entity.draw(screen, sprites, x, y)
    
    def click(self, holding: Entity | None) -> Entity | None:
        if holding is not None:
            if self.entity is None:
                self.entity = holding
                return None
            return holding

        if self.entity is not None:
            entity = self.entity
            self.entity = None
            return entity

        if self.buyable:
            return Entity(self.sprite)
        return None

    def ignite(self):
        if self.flammable:
            self.burning = True

    def extinguish(self):
        self.burning = False