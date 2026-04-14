import pygame
import json
import random

from screen import Screen
from sprites import Sprite
from board import Board

class MapScreen(Screen):
    def __init__(self, screen, width: int, height: int, sprites: dict[str, Sprite], player, level: int) -> None:
        super().__init__(screen, width, height, sprites, player, level)
        self.size = 32
        self.cloudeyisms = self.load_cloudeyisms('src/cloudeyisms.json')
        self.speech_text = self.cloudeyisms[0]
        self.speech_surface = None
        self.board = Board(45, 26)
        self.board.load_json('src/board.json')
        self.holding = None

    def load_cloudeyisms(self, path):
        with open(path) as file:
            return json.load(file)

    def draw(self) -> None:
        """
        Renders the screen
        """

        self.board.draw(self.screen, self.sprites)

        self.draw_speech()
        self.draw_cloudey()
        self.draw_selector()

    def tick(self) -> None:
        if random.randint(1, 60 * 10) == 1:
            self.speak(random.choice(self.cloudeyisms))
        self.board.tick()
    
    def speak(self, text):
        self.speech_text = text
        self.speech_surface = None

    def draw_speech(self):
        size = self.size
        max_width = 6 * size
        max_height = 3 * size

        if self.speech_surface is None:
            self.speech_surface = self.layout_text(self.speech_text,
                'comicsansms', 30, max_width, max_height)

        self.screen.blit(self.speech_surface, (size / 2, size / 2))

    # the approach here is fairly simple:
    # 1. ignore existing line breaks and instead split on whitespace.
    # 2. if that doesn't fit vertically, we'll shrink the text start over.
    # 3. finally, center the text vertically and horizontally.
    # i promise i've written better.
    def layout_text(self, text, font_name, font_size, max_width, max_height):
        font = pygame.font.SysFont(font_name, font_size)
        line_height = font.get_linesize()
        max_lines = max_height // line_height

        text = text.replace('\n', '').strip()
        words = text.split(' ')
        lines = []
        line = ''
        for word in words:
            (w, _) = font.size(line + ' ' + word)
            if w > max_width:
                lines.append(line)
                line = word
            else:
                line += ' ' + word

            if len(lines) >= max_lines:
                return self.layout_text(text, font_name, font_size - 1, max_width, max_height)
        lines.append(line)
            
        surface = pygame.Surface((max_width, max_height), pygame.SRCALPHA, 32)
        surface.convert_alpha()
        y = (max_height - len(lines) * line_height) // 2
        for line in lines:
            text_surface = font.render(line, True, (1, 1, 1))
            (w, _) = font.size(line)
            surface.blit(text_surface, ((max_width - w) // 2, y))
            y += line_height
        return surface

    def draw_cloudey(self):
        size = self.size
        cloudey_size = 4 * self.size
        (cursor_x, cursor_y) = pygame.mouse.get_pos()

        (cloudey_x, cloudey_y) = (2 * size, 4 * size)
        (center_x, center_y) = (cloudey_x + cloudey_size / 2, cloudey_y + cloudey_size / 2)

        if cursor_y < center_y:
            vertical = "top"
        elif cursor_y > (center_y + 10):
            vertical = "bottom"
        else:
            vertical = "center"

        if cursor_x >= (center_x + cloudey_size / 4):
            horizontal = "right"
        elif cursor_x <= (center_x - cloudey_size / 4):
            horizontal = "left"
        else:
            horizontal = "center"

        sprite = self.sprites[f"cloudey_{vertical}_{horizontal}"]
        
        sprite.draw(self.screen, (cloudey_x, cloudey_y), (cloudey_size, cloudey_size))

    def draw_selector(self):
        size = self.size
        (cursor_x, cursor_y) = pygame.mouse.get_pos()

        grid_x = cursor_x // size
        grid_y = cursor_y // size
        
        if self.holding is None:
            self.sprites['selector'].draw(self.screen,
                                    (grid_x * size, grid_y * size), (size, size))
        else:
            self.holding.pos = (grid_x, grid_y)
            self.holding.draw(self.screen, self.sprites)
    
    def on_event(self, event):
        """
        Responds to an individual pygame event. On screen change, returns the new screen
        """

        if event.type == pygame.KEYDOWN:
            if event.unicode == '\x08':
                self.speak(self.speech_text[:-1])
            elif event.unicode != '':
                self.speak(self.speech_text + event.unicode)
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.on_click(event.button, pygame.mouse.get_pos())

        return self
    
    def on_click(self, button, pos):
        (c_x, c_y) = pos
        (x, y) = (c_x // self.size, c_y // self.size)
        tile = self.board.tiles[x][y]

        if button == 1:
            print("clicked on tile", (x, y))
            self.holding = tile.click(self.holding)

        elif button == 3:
            if self.holding is not None:
                self.holding.kill()
                self.holding = None
            elif tile.entity is not None:
                tile.entity.kill()
                tile.entity = None