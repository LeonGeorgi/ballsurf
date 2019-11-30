import random

import numpy as np
import pygame
import pygame.gfxdraw
from scipy import interpolate

from const import Const
from context import Context
from gamerect import GameRect
from sprite import Sprite, Sprites, Type


class Hills(Sprite):

    def __init__(self):
        self.speed = 0.5

        self.control_points = []
        self.interpolation = None
        self.__x = -1
        self.cache = {}

    def update(self, context: Context, sprites: Sprites):
        self.__x += context.x_delta * self.speed
        changed = False
        while len(self.control_points) > 0 and self.control_points[0][0] - self.__x < -10:
            del self.control_points[0]
            changed = True

        left = Const.game_height * 4
        while len(self.control_points) == 0 or self.control_points[-1][0] - self.__x < left:
            if len(self.control_points) == 0:
                last = -10
            else:
                last = self.control_points[-1][0]
            self.control_points.append((last + 3, random.random()))
            changed = True

        if changed:
            self.interpolation = interpolate.splrep(*list(zip(*self.control_points)))
            self.cache = {}

    def render(self, surface: pygame.Surface, size_factor: float):
        if self.interpolation is None:
            return

        top = surface.get_height() * 0.5
        points = [(-10, surface.get_height() + 10)]
        for x in np.arange(int(-2 + self.__x), int(3 * Const.game_height + self.__x), 0.2):
            if x in self.cache:
                y = self.cache[x]
            else:
                y = interpolate.splev(x, self.interpolation) * size_factor + top
                self.cache[x] = y
            points.append(((x - self.__x) * size_factor, int(y)))
        points.append((surface.get_width() + 10, surface.get_height() + 10))

        pygame.gfxdraw.filled_polygon(surface, points, (65, 209, 98))
        pygame.gfxdraw.aapolygon(surface, points, (65, 209, 98))

    @property
    def box(self) -> GameRect:
        return GameRect(0, 0, 0, 0)

    def type(self) -> Type:
        return Type.HILLS
