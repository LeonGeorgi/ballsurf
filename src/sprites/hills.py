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
        self.speed = 0.3

        self.control_points = []
        self.interpolation = None
        self.__x = -1
        self.cache = {}

    def update(self, context: Context, sprites: Sprites):
        self.__x += context.x_delta * self.speed
        changed = False
        while len(self.control_points) > 0 and self.control_points[0][0] - self.__x < -20:
            del self.control_points[0]
            changed = True

        left = Const.game_height * 5
        while len(self.control_points) == 0 or self.control_points[-1][0] - self.__x < left:
            if len(self.control_points) == 0:
                last = -20
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

        step_size = int(size_factor * Const.pixel_size)

        top = surface.get_height() * 0.5
        points = []
        for x in np.arange(int(-2 + self.__x), int(3 * Const.game_height + self.__x), 1):
            if x in self.cache:
                y = self.cache[x]
            else:
                y = int(interpolate.splev(x, self.interpolation) * size_factor + top) // step_size * step_size
                self.cache[x] = y

            pos_x = int((x - self.__x) * size_factor)
            if len(points) > 0:
                last_x, last_y = points[-1]
                count = abs(last_y - y) // step_size
                if count > 0:
                    x_step = (pos_x - last_x) / count
                    y_step = (y - last_y) / count

                    points.append((
                        int(last_x + x_step),
                        int(last_y)
                    ))

                    for i in range(1, count):
                        points.append((
                            int(last_x + i * x_step),
                            int(last_y + i * y_step)
                        ))
                        points.append((
                            int(last_x + (i + 1) * x_step),
                            int(last_y + i * y_step)
                        ))
                else:
                    points.append((pos_x, y))
            else:
                points.append((pos_x, y))

        points.insert(0, (-10, surface.get_height() + 10))
        points.append((surface.get_width() + 10, surface.get_height() + 10))

        pygame.gfxdraw.filled_polygon(surface, points, (116, 156, 47))
        pygame.draw.lines(surface, (75, 102, 30), False, points, step_size)

    @property
    def box(self) -> GameRect:
        return GameRect(0, 0, 0, 0)

    def type(self) -> Type:
        return Type.HILLS
