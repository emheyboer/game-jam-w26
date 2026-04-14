import json
import random

from entity import Entity

def load_definitions(path):
    with open(path) as file:
        return json.load(file)

class Tile:
    size = 32
    definitions = load_definitions('src/tiles.json')
    def __init__(self, pos: tuple[int, int], name: str = '', kind: str = '',
                 burning = False) -> None:
        spec: dict = self.definitions[name] if name in self.definitions else {}

        self.pos = pos
        self.name = name
        self.kind = kind

        self.flammable: bool = spec.get('flammable') or False
        self.burning: bool = burning

        self.use_wind_direction = spec.get('use_wind_direction') or False
        self.direction = (1, 0)

        self.water_source = spec.get('water_source') or False

        self.health: int = spec.get('health') or 1

        self.sprite: str = spec['sprite'] if 'sprite' in spec else name
        if len(kind) > 0:
            self.sprite += '_' + kind
        
        self.buyable: bool = 'buyable' in spec
        if self.buyable:
            self.price: int = spec['buyable'].get('price') or 0
            self.buy_entity: str = spec['buyable']['entity']

        self.entity: Entity | None = None

    def draw(self, screen, sprites) -> None:
        size = self.size
        (x, y) = self.pos

        sprites['field_grassy'].draw(screen, (x * size, y * size), (size, size))
        sprite = self.sprite

        if self.use_wind_direction:
            (d_x, d_y) = self.direction
            suffix = ['top', 'center', 'bottom'][d_y + 1]
            suffix += '_'
            suffix += ['left', 'center', 'right'][d_x + 1]
            sprite += '_' + suffix

        # if a sprite has a dedicated 'burning' variant, we'll use that
        # otherwise, the generic fire sprite will suffice
        needs_fire = False
        if self.burning:
            if (sprite + '_burning') in sprites:
                sprite += '_burning'
            else:
                needs_fire = True

        if self.health <= 0:
            if (sprite + '_destroyed') in sprites:
                sprite += '_destroyed'
            else:
                sprite = 'destroyed'

        sprites[sprite].draw(screen, (x * size, y * size), (size, size))

        if needs_fire:
            sprites['fire'].draw(screen, (x * size, y * size), (size, size))

        if self.buyable:
            sprites['buyable'].draw(screen, (x * size, y * size), (size, size))

        if self.entity is not None:
            self.entity.draw(screen, sprites)
    
    def click(self, holding: Entity | None) -> Entity | None:
        if holding is not None:
            holding.pos = self.pos

        if holding is not None or self.entity is not None:
            tmp = self.entity
            self.entity = holding
            return tmp
        
        if self.buyable:
            return Entity(self.pos, self.buy_entity)
        return None

    def ignite(self):
        if self.flammable:
            self.burning = True

    def extinguish(self):
        self.burning = False

    def tick(self, board):
        if self.use_wind_direction:
            self.direction = board.wind_direction

        if self.entity is not None:
            self.entity.tick(board)

        if self.burning:
            self.health -= 1
            if self.health <= 0:
                self.extinguish()
                self.flammable = False
            if random.randint(1, 500) == 1:
                self.fire_spread(board)


    def fire_spread(self, board):
        """
        When trying to spread, we try to ignite the nearest tile in the same
        direction the wind is blowing. If that's not an option, try adjacent ones.
        """
        (x, y) = self.pos
        (dx, dy) = board.wind_direction
        (x, y) = (x + dx, y + dy)
        
        tile = board.find((x, y), lambda t : t.flammable and not t.burning, 1)
        if tile is not None:
            tile.ignite()