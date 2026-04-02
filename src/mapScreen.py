import pygame
import json
import random

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

        self.draw_mock_ui()

        self.draw_smoky()
        self.draw_selector()
    
    def draw_mock_ui(self):
        size = self.size
        columns = self.width // size
        rows = self.height // size
    
        for x in range(0, columns):
            for y in range(0, rows):
                self.sprites['field_grassy'].draw(self.screen,
                                                (x * size, y * size), (size, size))

        # yes, we are in fact loading json 60 times/s
        # no, there's not a good reason for this
        with open('src/board.json') as file:
            board = json.load(file)
        for region in board:
            for x in range(region['cols'][0], region['cols'][1] + 1):
                for y in range(region['rows'][0], region['rows'][1] + 1):
                    self.sprites[region['sprite']].draw(self.screen,
                                                (x * size, y * size), (size, size))
                    
        # don't hate me, i'll redraw these later so they're not so weird
        self.sprites['1'].draw(self.screen,
                                    (3.5 * size, 6.5 * size), (1.5 * size, 1.5 * size))
        self.sprites['0'].draw(self.screen,
                                    (4.5 * size, 6.5 * size), (1.5 * size, 1.5 * size))
        self.sprites['2'].draw(self.screen,
                                    (3.5 * size, 8.5 * size), (1.5 * size, 1.5 * size))
        self.sprites['7'].draw(self.screen,
                                    (4.5 * size, 8.5 * size), (1.5 * size, 1.5 * size))

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
        
        sprite.draw(self.screen, (2 * size, 1 * size), (smoky_size, smoky_size))

    def draw_selector(self):
        size = self.size
        (cursor_x, cursor_y) = pygame.mouse.get_pos()

        grid_x = cursor_x // size
        grid_y = cursor_y // size
        
        self.sprites['selector'].draw(self.screen,
                                    (grid_x * size, grid_y * size), (size, size))
    
    def on_event(self, event):
        """
        Responds to an individual pygame event. On screen change, returns the new screen
        """

        if event.type == pygame.KEYUP:
            if event.unicode == '>':
                self.size <<= 1
            elif event.unicode == '<':
                self.size >>= 1

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            (c_x, c_y) = pygame.mouse.get_pos()
            grid_pos = (c_x // self.size, c_y // self.size)
            print(grid_pos)

        return self