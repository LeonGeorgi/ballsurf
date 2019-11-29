import pygame

from context import Context
from gamerect import GameRect
from sprite import Sprite, Sprites


class Nicholas(Sprite):

    def __init__(self):
        self.__vpos = 0.5
        self.__vspeed = -0.01

    def update(self, context: Context, sprites: Sprites):
        t = context.time_factor * 5
        self.__vpos = 1 / 2 * context.gravity * (t ** 2) + \
                      self.__vspeed * t + \
                      self.__vpos
        self.__vspeed = context.gravity * t + self.__vspeed
        if self.__vpos >= 0.9:
            self.__vspeed = -abs(self.__vspeed)

    def render(self, surface: pygame.Surface, size_factor: float):
        surface.fill((0, 200, 0), self.box.to_pygame(size_factor))

    @property
    def box(self) -> GameRect:
        return GameRect(0.1, self.__vpos, 0.1, 0.1)
