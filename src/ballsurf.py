import sys

import pygame
from pygame.locals import *

from src.world import World


def run():
    pygame.init()

    fps = 60
    fps_clock = pygame.time.Clock()

    width, height = 640, 480
    screen: pygame.Surface = pygame.display.set_mode((width, height))

    world = World()

    # Game loop.
    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        world.update()

        world.render(screen)

        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == '__main__':
    run()
