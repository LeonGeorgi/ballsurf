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
            self.x = 2 * Const.game_height
        else:
            self.x = x

        self.image = CachedImage(self.filename())
        self.diameter = self.image.get_width() * Const.pixel_size

        self.y = Const.game_height - self.diameter
        self.__vspeed = 0
        self.bounced = False
        self.hit_bottom = False

        self.id = uuid.uuid4()

    def update(self, context: Context, sprites: Sprites):
        self.x -= context.x_delta
        if self.bounced:
            self.move_by_gravity(context)

    def render(self, surface: pygame.Surface, size_factor: float):
        d = int(self.diameter * size_factor)
        img = self.image.scale(d, d)
        surface.blit(img, (self.x * size_factor, self.y * size_factor))

    def bounce(self, velocity: float):
        self.bounced = True
        self.__vspeed = velocity / 2

    def move_by_gravity(self, context: Context):

        # time in s
        t = context.time_factor / Const.fps
        # gravity in m/(s**2)
        a = context.gravity
        self.y = 1 / 2 * a * (t ** 2) + \
                      self.__vspeed * t + \
                      self.y
        self.__vspeed = a * t + self.__vspeed
        if self.y + self.diameter >= Const.game_height and not self.hit_bottom:
            self.__vspeed = -self.__vspeed * self.bounciness()
            self.hit_bottom = True
        elif self.y + self.diameter < Const.game_height and self.hit_bottom:
            self.hit_bottom = False



    @property
    def box(self) -> GameRect:
        return GameRect(self.x, self.y, self.diameter, self.diameter)

    def type(self) -> Type:
        return Type.BALL

    def can_delete(self) -> bool:
        return self.x <= -1

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
