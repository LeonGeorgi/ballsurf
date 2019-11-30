import math
import random

import pygame

from const import Const
from context import Context
from sprite import Sprites
from sprites.background import Background, BackgroundType
from sprites.balls.regular_ball import RegularBall
from sprites.balls.small_ball import SmallBall
from sprites.nicholas import Nicholas


class World:
    def __init__(self):
        self.sprites = Sprites([Background(BackgroundType.BACKGROUND), Background(BackgroundType.MIDDLE_GROUND),
                                Background(BackgroundType.FOREGROUND),
                                Nicholas()])
        self.x = 0
        self.time = 0
        self.countdown = Const.countdown

    def __update_balls(self, context: Context):
        balls = list(self.sprites.get_balls())

        del_balls = []
        for ball in balls:
            if ball.can_delete():
                del_balls.append(ball)

        for ball in del_balls:
            self.sprites.remove(ball)
            balls.remove(ball)

        if len(balls) < 10 and random.random() < 0.05:
            if random.random() < 0.5:
                ball = RegularBall()
            else:
                ball = SmallBall()
            if not any(b.box.intersects_with(ball.box) for b in balls):
                self.sprites.append(ball)

    def update(self, context: Context):
        self.time = math.floor(context.running_time)
        self.countdown = Const.countdown - self.time

        self.__update_balls(context)

        for sprite in self.sprites:
            sprite.update(context, self.sprites)

    def render(self, surface: pygame.Surface, size_factor: float):
        for sprite in self.sprites:
            sprite.render(surface, size_factor)

        if self.countdown >= 0:
            font = pygame.font.Font("../res/Game_font.ttf", surface.get_height() // 5)
            img = font.render(str(self.countdown), True, (0, 0, 0))
            surface.blit(img, (
                surface.get_width() // 2 - img.get_width() // 2,
                surface.get_height() // 2 - img.get_height() // 2
            ))
        else:
            font = pygame.font.Font("../res/Game_font.ttf", surface.get_height() // 10)
            img = font.render(str(self.time), True, (0, 0, 0))
            surface.blit(img, (int(surface.get_width() * 0.95) - img.get_width(), int(surface.get_height() * 0.05)))
