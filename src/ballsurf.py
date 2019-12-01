import sys

import pygame
from pygame.locals import *

from const import Const
from context import Context, Key
from game import Game
from image import CachedImage


def run():
    pygame.init()

    pygame.display.set_caption("Ballsurf")

    fps = 60
    default_millis = 1000 / fps
    fps_clock = pygame.time.Clock()

    width, height = 1280, 720
    screen: pygame.Surface = pygame.display.set_mode((width, height))

    game = Game()
    context = Context()

    # Game loop.
    while True:
        screen.fill((0, 0, 0))

        context.key_strokes = set()
        context.resize = False
        context.letter = ''

        # Get system events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.dict['size']
                pygame.display.set_mode((width, height))
                context.resize = True
                CachedImage.clear_cache()

            if event.type == pygame.KEYDOWN:
                if event.key == 8:
                    context.key_strokes.add(Key.BACKSPACE)
                else:
                    context.letter = event.unicode

        # Key key strokes
        keys = pygame.key.get_pressed()
        if keys[K_SPACE] or keys[K_RETURN]:
            context.key_strokes.add(Key.ACTION)
        if keys[K_DOWN]:
            context.key_strokes.add(Key.NEXT)
        if keys[K_UP]:
            context.key_strokes.add(Key.PREV)
        if keys[K_ESCAPE]:
            context.key_strokes.add(Key.ESCAPE)

        game.update(context)

        size = min(width, height)
        game.render(screen, size / Const.game_height)

        pygame.display.flip()
        context.time_factor = fps_clock.tick(fps) / default_millis


if __name__ == '__main__':
    run()
