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
        self.__last_ball = None

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
        last_ball = self.__last_ball
        self.__last_ball = None
        for ball in sprites.get_balls():
            if self.box.intersects_with(ball.box):
                self.__last_ball = ball.id
                break

        if last_ball != self.__last_ball:
            self.__bounced = False

        if self.__last_ball is not None and not self.__bounced:
            self.__bounced = True
            self.bounce(context, ball.bounciness())
        elif last_ball is None:
            self.__bounced = False
        # if self.__vspeed < Const.game_height - self.__height and self.__bounced:
        #    self.__bounced = False

    def bounce(self, context: Context, ball_factor: float):
        new_speed = -self.__vspeed * ball_factor * context.ball_factor_factor
        minimum_velocity = -math.sqrt(2 * context.gravity * self.__vpos)
        self.__vspeed = max(new_speed, minimum_velocity)

    def render(self, surface: pygame.Surface, size_factor: float):
        surface.fill((0, 200, 0), self.box.to_pygame(size_factor))

    @property
    def box(self) -> GameRect:
        return GameRect(Const.game_height * 0.2, self.__vpos, self.__height, self.__height)

    def type(self) -> Type:
        return Type.PLAYER
