#!/usr/bin/env python3
import pygame

from sprites import load_sprites
from screen import Screen

def main():
    pygame.init()
    pygame.display.set_caption('disappointing smoky the bear')

    screen = pygame.display.set_mode()
    width, height = pygame.display.get_surface().get_size()

    clock = pygame.time.Clock()

    sprites = load_sprites()

    player = {}
    current_screen = Screen(screen, width, height, sprites, player, 0)

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

        if keys[pygame.K_q]:
            running = False

        screen.fill((0, 0, 0))

        current_screen.draw()

        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
