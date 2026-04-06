#!/usr/bin/env python3
import pygame

from sprites import load_sprites
from mapScreen import MapScreen

def main():
    pygame.init()
    # (｡•̀ᴗ-)✧ Super Dissapointing 
    pygame.display.set_caption('disappointing smoky the bear')

    pygame.mouse.set_visible(False)

    screen = pygame.display.set_mode((45 * 32, 26 * 32))
    width, height = pygame.display.get_surface().get_size()

    clock = pygame.time.Clock()

    sprites = load_sprites()

    player = {}
    current_screen = MapScreen(screen, width, height, sprites, player, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                current_screen = current_screen.on_event(event)

                if current_screen == "retry":
                    return main()

                

        keys = pygame.key.get_pressed()
        # Me reading through the code and about to add a quit button
        # then getting to here /(ᵒ̤̑ ₀̑ ᵒ̤̑/) wow!*✰
        if keys[pygame.K_ESCAPE]:
            running = False

        screen.fill((0, 0, 0))

        current_screen.tick()

        current_screen.draw()

        (c_x, c_y) = pygame.mouse.get_pos() 
        sprites['cursor'].draw(screen, (c_x - 16, c_y - 8), (32, 32))

        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
