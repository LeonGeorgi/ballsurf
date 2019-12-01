import random

import pygame

import score
from const import Const
from context import Context
from gamerect import GameRect
from image import CachedImage
from sprite import Sprite, Sprites, Type


class Tartan(Sprite):

    def __init__(self):
        self.__x = 0
        self.meters = Const.offset_meters
        self.image = CachedImage("../res/img/noice.png")
        self.border = self.image.get_width() * Const.pixel_size
        self.random_line = [-1, 1]

        self.score = score.load_score()

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

        t = int((Const.tartan_top + Const.pixel_size) * size_factor)
        h = int(Const.tartan_height * 0.38 * size_factor)
        lines = [
            t,
            t + h,
            t + 2 * h
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
        next_meter_in = m - (self.meters - Const.player_position) % m
        next_meter_str = str(int(((self.meters - Const.player_position) // m + 1) * m))
        surface.fill((255, 200, 200),
                     pygame.Rect(
                         int(next_meter_in * size_factor),
                         lines[0],
                         int(size_factor * Const.pixel_size),
                         h
                     ))
        font = pygame.font.Font("../res/arcade.ttf", h)
        img = font.render(next_meter_str, True, (255, 200, 200))
        surface.blit(img, (int((next_meter_in - 2 * Const.pixel_size) * size_factor) - img.get_width(),
                           int(lines[0] + h / 2 - img.get_height() * 0.45)))

        surface.fill((255, 200, 200),
                     pygame.Rect(
                         int(self.random_line[0] * size_factor),
                         lines[self.random_line[1]],
                         int(size_factor * Const.pixel_size),
                         h
                     ))

        PADDING = Const.pixel_size * 2
        for i, (name, s) in enumerate(self.score):
            left = s - (self.meters - Const.player_position)
            if -Const.game_height < left < Const.game_height * 3:
                text = f"{i + 1}   {name}".rstrip()
                img = font.render(text, True, (255, 255, 255))

                pixel = int(Const.pixel_size * size_factor)
                surface.fill((133, 94, 66),
                             pygame.Rect(
                                 int(left * size_factor) - pixel,
                                 int(Const.tartan_top * size_factor - h),
                                 int(size_factor * Const.pixel_size) + 2 * pixel,
                                 h
                             ))

                l = int((left - PADDING) * size_factor - img.get_width() // 2)
                surface.fill((106, 75, 53),
                             pygame.Rect(
                                 max(0, l - pixel),
                                 int(Const.tartan_top * size_factor - h * 1.5) - pixel,
                                 img.get_width() + PADDING * 2 * size_factor + min(0, l) + 2 * pixel,
                                 img.get_height() + 2 * pixel
                             ))

                surface.fill((133, 94, 66),
                             pygame.Rect(
                                 max(0, l),
                                 int(Const.tartan_top * size_factor - h * 1.5),
                                 img.get_width() + PADDING * 2 * size_factor + min(0, l),
                                 img.get_height()
                             ))

                surface.blit(img, (
                    int(left * size_factor - img.get_width() // 2),
                    int(Const.tartan_top * size_factor - h * 1.5)
                ))

    def box(self) -> GameRect:
        return GameRect(0, 0, 1, 1)

    def type(self) -> Type:
        return Type.TARTAN
