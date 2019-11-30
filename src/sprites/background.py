from enum import IntEnum

import pygame
import pygame.gfxdraw

from const import Const
from context import Context
from gamerect import GameRect
from sprite import Sprite, Sprites, Type


class BackgroundType(IntEnum):
    FOREGROUND = 3
    MIDDLE_GROUND = 2
    BACKGROUND = 1


class Background(Sprite):

    def type(self) -> Type:
        return Type.BACKGROUND

    def __init__(self, bg_type: BackgroundType):
        self.__bg_type = bg_type
        if self.__bg_type == BackgroundType.FOREGROUND:
            self.speed_factor = 1.0
        elif self.__bg_type == BackgroundType.MIDDLE_GROUND:
            self.speed_factor = 0.66
        else:
            self.speed_factor = 0.33
        self.__x = 0
        self.__count = 12

    def update(self, context: Context, sprites: Sprites):
        self.__x = (self.__x - context.x_delta * self.speed_factor * self.__count / Const.game_height) % 2.0

    def render(self, surface: pygame.Surface, size_factor: float):
        size = size_factor * Const.game_height / self.__count
        flag = False
        x_diff = self.__x * size
        for x in range(-2, self.__count * 2):
            for y in range(self.__count // 3):
                surface.fill((200, 200, 200) if flag else (255, 255, 255),
                             pygame.Rect(x_diff + x * size, (y + ((self.__bg_type.value - 1) * self.__count //
                                                                  3)) * size, size,
                                         size))
                flag = not flag
            flag = not flag

    @property
    def box(self) -> GameRect:
        return GameRect(self.__x, 0.9, 0.10, 0.10)
