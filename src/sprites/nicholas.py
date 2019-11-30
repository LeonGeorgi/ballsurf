import math

import pygame

from const import Const
from context import Context, Key
from gamerect import GameRect
from sprite import Sprite, Sprites, Type


class Nicholas(Sprite):

    def __init__(self):
        self.__vpos = 0.5
        self.__vspeed = -0.005
        self.__height = 1
        self.__vpos_max = 1 - self.__height
        self.__bounced = False

    def move_by_gravity(self, context: Context):
        # time in s
        t = context.time_factor / Const.fps
        # gravity in m/(s**2)
        a = context.gravity

        if Key.MAIN in context.key_strokes and (self.__vspeed >= 0 or self.__vpos < 0.5 * Const.game_height):
            context.current_speed = (context.current_speed - context.desired_speed) * math.pow(
                context.speed_factor_dec, context.time_factor) + context.desired_speed
            a *= 4

        self.__vpos = 1 / 2 * a * (t ** 2) + \
                      self.__vspeed * t + \
                      self.__vpos
        self.__vspeed = a * t + self.__vspeed

    def update(self, context: Context, sprites: Sprites):
        if math.floor(context.running_time) <= Const.countdown:
            return

        self.move_by_gravity(context)
        intersected = False
        for ball in sprites.get_balls():
            if self.box.intersects_with(ball.box):
                intersected = True
                break

        if intersected and not self.__bounced:
            self.__bounced = True
            # noinspection PyUnboundLocalVariable
            self.__vspeed = -abs(self.__vspeed) * ball.bounciness()
            v0 = -math.sqrt(2 * context.gravity * self.__vpos)
            if v0 > self.__vspeed:
                self.__vspeed = v0
        elif self.__vspeed < Const.game_height - self.__height and self.__bounced:
            self.__bounced = False

    def render(self, surface: pygame.Surface, size_factor: float):
        surface.fill((0, 200, 0), self.box.to_pygame(size_factor))

    @property
    def box(self) -> GameRect:
        return GameRect(Const.game_height * 0.2, self.__vpos, self.__height, self.__height)

    def type(self) -> Type:
        return Type.PLAYER
