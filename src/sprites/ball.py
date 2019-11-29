import pygame
import pygame.gfxdraw

from context import Context
from gamerect import GameRect
from sprite import Sprite, Sprites


class Ball(Sprite):

    def __init__(self):
        self.__x = 2

    def update(self, context: Context, sprites: Sprites):
        self.__x -= context.x_delta

    def render(self, surface: pygame.Surface, size_factor: float):
        pygame.gfxdraw.filled_ellipse(surface, *self.box.to_ellipse_data(size_factor), (0, 0, 200))
        pygame.gfxdraw.aaellipse(surface, *self.box.to_ellipse_data(size_factor), (0, 0, 200))

    @property
    def box(self) -> GameRect:
        return GameRect(self.__x, 0.9, 0.10, 0.10)
