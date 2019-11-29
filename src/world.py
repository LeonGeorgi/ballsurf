import pygame

from context import Context, Key
from sprite import Sprites
from sprites.nicholas import Nicholas
from sprites.ball import Ball
import random


class World:
    def __init__(self):
        self.sprites = Sprites([Nicholas()])
        self.x = 0
        self.pressed = False

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
            ball = Ball()
            if not any(b.box.intersects_with(ball.box) for b in balls):
                self.sprites.append(Ball())

    def update(self, context: Context):
        self.x = (self.x - context.x_delta * 8) % 2.0

        self.pressed = Key.MAIN in context.key_strokes

        self.__update_balls(context)

        for sprite in self.sprites:
            sprite.update(context, self.sprites)

    def render(self, surface: pygame.Surface, size_factor: float):
        count = 8
        size = size_factor / count
        flag = False
        x_diff = self.x * size
        for x in range(-2, count * 2):
            for y in range(count):
                surface.fill((200, 200, 200) if flag else (255, 255, 255),
                             pygame.Rect(x_diff + x * size, y * size, size, size))
                flag = not flag
            flag = not flag

        if self.pressed:
            surface.fill((255, 0, 0),
                         pygame.Rect(0.4 * size_factor, 0.4 * size_factor, 0.2 * size_factor, 0.2 * size_factor))

        for sprite in self.sprites:
            sprite.render(surface, size_factor)
