import uuid
from abc import abstractmethod, ABC

import pygame.gfxdraw

from const import Const
from context import Context
from gamerect import GameRect
from image import CachedImage
from sprite import Sprite, Sprites, Type


class Ball(Sprite, ABC):

    def __init__(self, x=None):
        if x is None:
            self.__x = 2 * Const.game_height
        else:
            self.__x = x * Const.game_height

        self.image = CachedImage(self.filename())
        self.diameter = self.image.get_width() * Const.pixel_size

        self.id = uuid.uuid4()

    def update(self, context: Context, sprites: Sprites):
        self.__x -= context.x_delta

    def render(self, surface: pygame.Surface, size_factor: float):
        d = int(self.diameter * size_factor)
        img = self.image.scale(d, d)
        surface.blit(img, (self.__x * size_factor, (Const.game_height - self.diameter) * size_factor))

    @property
    def box(self) -> GameRect:
        return GameRect(self.__x, Const.game_height - self.diameter, self.diameter, self.diameter)

    def type(self) -> Type:
        return Type.BALL

    def can_delete(self) -> bool:
        return self.__x <= -1

    @abstractmethod
    def filename(self) -> str:
        pass

    @abstractmethod
    def bounciness(self) -> float:
        """
        :return: by how much the velocity of the player is multiplied when he hits the ball
        """
        pass

    @abstractmethod
    def immediate_speed_increase(self) -> float:
        pass

    @abstractmethod
    def desired_speed_increase(self) -> float:
        pass
