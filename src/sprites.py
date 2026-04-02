import pygame
import json

class SpriteSheet:
    def __init__(self, path: str) -> None:
        self.path = path
        self.surface = pygame.image.load(path).convert()

class Sprite:
    def __init__(self, spriteSheet: SpriteSheet, pos: tuple[int, int], size: tuple[int, int],
                 textOffset: tuple[int, int] = (0, 0), fontSize: int = 30) -> None:
        self.x, self.y = pos
        self.width, self.height = size
        self.offsetX, self.offsetY = textOffset
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), fontSize)

        self.sprite = pygame.Surface(size)
        self.sprite.set_colorkey((0,0,0))
        self.sprite.blit(spriteSheet.surface, (0, 0), (self.x, self.y, self.width, self.height))

    def draw(self, screen, pos: tuple[float, float], size = None, text = None, scaleText: bool = True):
        x, y = pos
        sprite = self.sprite.copy()
        
        if text is not None and scaleText:
            text_surface = self.font.render(text, False, (1, 1, 1))
            sprite.blit(text_surface, (self.offsetX, self.offsetY))

        if size is not None:
            sprite = pygame.transform.scale(sprite, size)

        if text is not None and not scaleText:
            text_surface = self.font.render(text, False, (1, 1, 1))
            sprite.blit(text_surface, (self.offsetX, self.offsetY))

        screen.blit(sprite, (x, y))


def load_sprites():
    sprites = {}

    mapping = None
    with open('assets/sprites.json') as file:
        mapping = json.load(file)

    for path in mapping:
        info = mapping[path]
        sheet = SpriteSheet('assets/' + path)
        [w, h] = [int(n) for n in info['size'].split('x')]
        for x in range(0, info['cols']):
            for y in range(0, info['rows']):
                sprite = Sprite(sheet, (w * x, h * y), (w, h))
                sprites[info['sprites'][y][x]] = sprite

    return sprites