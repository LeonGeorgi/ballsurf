import pygame

from context import Context, Key
from gamerect import GameRect
from sprite import Sprite, Sprites


class Nicholas(Sprite):

    def __init__(self):
        self.__vpos = 0.5
        self.__vspeed = -0.005
        self.__bounced = False

    def update(self, context: Context, sprites: Sprites):
        t = context.time_factor * 5
        a = context.gravity
        if Key.MAIN in context.key_strokes and self.__vspeed >= 0:
            a *= 2
        self.__vpos = 1 / 2 * a * (t ** 2) + \
                      self.__vspeed * t + \
                      self.__vpos
        self.__vspeed = a * t + self.__vspeed
        if self.__vpos >= 0.9 and not self.__bounced:
            self.__bounced = True
            self.__vspeed = -abs(self.__vspeed) * 0.9
        elif self.__vspeed < 0.9 and self.__bounced:
            self.__bounced = False

    def render(self, surface: pygame.Surface, size_factor: float):
        surface.fill((0, 200, 0), self.box.to_pygame(size_factor))

    @property
    def box(self) -> GameRect:
        return GameRect(0.1, self.__vpos, 0.1, 0.1)