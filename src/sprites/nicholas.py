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
        ball_bounciness = 0
        for ball in sprites.get(Type.BALL):
            if self.box.intersects_with(ball.box):
                self.__last_ball = ball.id
                ball_bounciness = ball.bounciness()
                break

        if self.__last_ball is None:
            # check if player hits the bottom
            if self.__vpos + self.__height >= Const.game_height:
                # player hits the bottom
                self.__last_ball = 0
                ball_bounciness = 0.3

        if last_ball != self.__last_ball:
            self.__bounced = False

        intersected = self.__last_ball is not None

        if intersected:

            if not self.__bounced:
                self.__bounced = True
                if self.__last_ball == 0:

                    # bounce from bottom
                    self.bounce_from_bottom(context, ball_bounciness)
                else:
                    self.bounce_from_ball(context, ball_bounciness)

            if self.__vpos + self.__height >= Const.game_height and self.__vspeed > 0:
                context.lost = True

    def bounce(self, input_speed: float, context: Context, bounciness: float):
        minimum_velocity = -math.sqrt(2 * context.gravity * self.__vpos)
        new_speed = -input_speed * bounciness * context.ball_factor_factor
        self.__vspeed = max(new_speed, minimum_velocity)

    def bounce_from_ball(self, context: Context, bounciness: float):
        input_speed = max(5, abs(self.__vspeed))
        self.bounce(input_speed, context, bounciness)

    def bounce_from_bottom(self, context: Context, bounciness: float):
        self.bounce(self.__vspeed, context, bounciness)

    def render(self, surface: pygame.Surface, size_factor: float):
        surface.fill((0, 200, 0), self.box.to_pygame(size_factor))

    @property
    def box(self) -> GameRect:
        return GameRect(Const.game_height * 0.2, self.__vpos, self.__height, self.__height)

    def type(self) -> Type:
        return Type.PLAYER
