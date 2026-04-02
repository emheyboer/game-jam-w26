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
                if x >= 8:
                    self.sprites['forest'].draw(self.screen,
                                                (x * size, y * size), (size, size))
                    
        self.draw_smoky()

    def draw_smoky(self):
        size = self.size
        smoky_size = 4 * self.size
        (cursor_x, cursor_y) = pygame.mouse.get_pos()

        (smoky_x, smoky_y) = (2 * size, 1 * size)
        (center_x, center_y) = (smoky_x + smoky_size / 2, smoky_y + smoky_size / 2)

        vertical = "top" if cursor_y < center_y else "bottom"

        if cursor_x >= (center_x + smoky_size / 4):
            horizontal = "right"
        elif cursor_x <= (center_x - smoky_size / 4):
            horizontal = "left"
        else:
            horizontal = "center"

        sprite = self.sprites[f"smoky_{vertical}_{horizontal}"]
        print(f"smoky_{vertical}_{horizontal}", sprite)
        
        sprite.draw(self.screen, (2 * size, 1 * size), (smoky_size, smoky_size))
    
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