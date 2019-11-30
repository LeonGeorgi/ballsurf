import pygame

from const import Const
from context import Context
from gamerect import GameRect
from sprite import Sprite, Sprites, Type


class Tartan(Sprite):

    def __init__(self):
        self.__x = 0
        self.image = pygame.image.load("../res/img/noice.png")
        self.border = self.image.get_width() * Const.pixel_size

    def update(self, context: Context, sprites: Sprites):
        self.__x -= context.x_delta
        while self.__x < -self.border:
            self.__x += self.border

    def render(self, surface: pygame.Surface, size_factor: float):
        area = Const.tartan_area(surface)
        surface.fill((156, 67, 47), area)

        size = int(self.image.get_width() * Const.pixel_size * size_factor)
        img = pygame.transform.scale(self.image, (size, size))

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

    def box(self) -> GameRect:
        return GameRect(0, 0, 1, 1)

    def type(self) -> Type:
        return Type.TARTAN
