import pygame

from sprite import Sprites
from sprites.nicholas import Nicholas
from sprites.ball import Ball
from context import Context, Key


class World:
    def __init__(self):
        self.sprites = Sprites([Nicholas(), Ball()])
        self.x = 0
        self.pressed = False

    def update(self, context: Context):
        self.x = (self.x - context.x_delta * 8) % 2.0

        self.pressed = Key.MAIN in context.key_strokes

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
