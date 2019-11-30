import random

import pygame

from const import Const
from context import Context
from gamerect import GameRect
from image import CachedImage
from sprite import Sprite, Sprites, Type


class Tartan(Sprite):

    def __init__(self):
        self.__x = 0
        self.meters = 0.0
        self.image = CachedImage("../res/img/noice.png")
        self.border = self.image.get_width() * Const.pixel_size
        self.random_line = [-1, 1]

    def update(self, context: Context, sprites: Sprites):
        self.__x -= context.x_delta
        self.meters = context.meters
        while self.__x < -self.border:
            self.__x += self.border

        self.random_line[0] -= context.x_delta
        if self.random_line[0] < 0 and random.random() < 0.05:
            self.random_line[0] = 3 * Const.game_height
            self.random_line[1] = random.randint(1, 2)

    def render(self, surface: pygame.Surface, size_factor: float):
        area = Const.tartan_area(surface)
        surface.fill((156, 67, 47), area)

        size = int(self.image.get_width() * Const.pixel_size * size_factor)
        img = self.image.scale(size, size)

        for i in range(0, surface.get_width() // size + 2):
            surface.blit(img, (i * size + self.__x * size_factor, area.top))

        lines = [
            int(Const.game_height * size_factor * 0.82),
            int(Const.game_height * size_factor * 0.89),
            int(Const.game_height * size_factor * 0.96)
        ]

        for y in lines:
            for x in range(0, 3 * Const.game_height):
                surface.fill((255, 200, 200),
                             pygame.Rect(
                                 int((x + self.__x) * size_factor),
                                 y,
                                 int(size_factor * 1),
                                 int(size_factor * Const.pixel_size)
                             ))

        m = 50
        next_meter_in = m - self.meters % m
        next_meter_str = str(int((self.meters // m + 1) * m))
        surface.fill((255, 200, 200),
                     pygame.Rect(
                         int(next_meter_in * size_factor),
                         lines[0],
                         int(size_factor * Const.pixel_size),
                         int(Const.game_height * size_factor * 0.07 + size_factor * Const.pixel_size)
                     ))
        font = pygame.font.Font("../res/arcade.ttf", int(Const.game_height * size_factor * 0.07))
        img = font.render(next_meter_str, True, (255, 200, 200))
        surface.blit(img, (int((next_meter_in - 2 * Const.pixel_size) * size_factor) - img.get_width(),
                           int(lines[0] + Const.game_height * size_factor * 0.038 - img.get_height() // 2)))

        surface.fill((255, 200, 200),
                     pygame.Rect(
                         int(self.random_line[0] * size_factor),
                         lines[self.random_line[1]],
                         int(size_factor * Const.pixel_size),
                         int(Const.game_height * size_factor * 0.07 + size_factor * Const.pixel_size)
                     ))

    def box(self) -> GameRect:
        return GameRect(0, 0, 1, 1)

    def type(self) -> Type:
        return Type.TARTAN
