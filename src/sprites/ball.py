from abc import abstractmethod, ABC
from typing import Tuple

import pygame
import pygame.gfxdraw

from const import Const
from context import Context
from gamerect import GameRect
from sprite import Sprite, Sprites, Type


class Ball(Sprite, ABC):

    def __init__(self):
        self.__x = 2 * Const.game_height

    def update(self, context: Context, sprites: Sprites):
        self.__x -= context.x_delta

    def render(self, surface: pygame.Surface, size_factor: float):
        pygame.gfxdraw.filled_ellipse(surface, *self.box.to_ellipse_data(size_factor), self.color())
        pygame.gfxdraw.aaellipse(surface, *self.box.to_ellipse_data(size_factor), self.color())

    @property
    def box(self) -> GameRect:
        return GameRect(self.__x, Const.game_height - self.diameter(), self.diameter(), self.diameter())

    def type(self) -> Type:
        return Type.BALL

    def can_delete(self) -> bool:
        return self.__x <= -1

    @abstractmethod
    def diameter(self) -> float:
        """
        :return: the diameter of the ball in meter
        """
        pass

    @abstractmethod
    def bounciness(self) -> float:
        """
        :return: by how much the velocity of the player is multiplied when he hits the ball
        """
        pass

    @abstractmethod
    def color(self) -> Tuple[int, int, int]:
        pass
