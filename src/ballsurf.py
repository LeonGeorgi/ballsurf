import sys

import pygame
from pygame.locals import *

from src.context import Context, Key
from src.world import World


def run():
    pygame.init()

    fps = 60
    default_millis = 1000 / fps
    speed_factor = 1 / (fps * 60)
    delta_factor = 1 / fps
    fps_clock = pygame.time.Clock()

    width, height = 640, 480
    screen: pygame.Surface = pygame.display.set_mode((width, height))

    world = World()
    context = Context()

    # Game loop.
    while True:
        screen.fill((0, 0, 0))

        context.key_strokes = set()

        # Get system events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.dict['size']
                pygame.display.set_mode((width, height))

        # Key key strokes
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            context.key_strokes.add(Key.MAIN)
        if keys[K_q]:
            pygame.quit()
            sys.exit()

        context.speed += speed_factor * context.time_factor
        context.x_delta = -delta_factor * context.speed * context.time_factor

        world.update(context)

        size = min(width, height)
        world.render(screen, size)

        pygame.display.flip()
        context.time_factor = fps_clock.tick(fps) / default_millis


if __name__ == '__main__':
    run()
