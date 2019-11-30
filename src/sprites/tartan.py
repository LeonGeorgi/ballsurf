import pygame

from const import Const
from context import Context
from gamerect import GameRect
from sprite import Sprite, Sprites, Type


class Tartan(Sprite):

    def __init__(self):
        self.__x = 0

    def update(self, context: Context, sprites: Sprites):
        self.__x -= context.x_delta
        while self.__x < -1:
            self.__x += 1

    def render(self, surface: pygame.Surface, size_factor: float):
        surface.fill((156, 67, 47), Const.tartan_area(surface))

        lines = [
            int(Const.game_height * size_factor * 0.82),
            int(Const.game_height * size_factor * 0.89),
            int(Const.game_height * size_factor * 0.96)
        ]

        for y in lines:
            for x in range(0, 2 * Const.game_height):
                surface.fill((255, 200, 200),
                             pygame.Rect(
                                 int((x + self.__x) * size_factor),
                                 y,
                                 int(size_factor * 1),
                                 int(size_factor * Const.pixel_size)
                             ))

    def box(self) -> GameRect:
        return GameRect(0, 0, 1, 1)

    def type(self) -> Type:
        return Type.TARTAN
