import pygame

from screen import Screen
from sprites import Sprite

class MapScreen(Screen):
    def __init__(self, screen, width: int, height: int, sprites: dict[str, Sprite], player, level: int) -> None:
        super().__init__(screen, width, height, sprites, player, level)
        self.size = 32

    def draw(self) -> None:
        """
        Renders the screen
        """
        size = self.size
        columns = self.width // size
        rows = self.height // size
        for x in range(0, columns):
            for y in range(0, rows):
                self.sprites['field_grassy'].draw(self.screen,
                                                (x * size, y * size), (size, size))
                self.sprites['forest'].draw(self.screen,
                                                (x * size, y * size), (size, size))
    
    def on_event(self, event):
        """
        Responds to an individual pygame event. On screen change, returns the new screen
        """

        if event.type == pygame.KEYUP:
            if event.unicode == '>':
                self.size <<= 1
            elif event.unicode == '<':
                self.size >>= 1
            print(self.size)

        return self