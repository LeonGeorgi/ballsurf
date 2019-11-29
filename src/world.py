import pygame

from src.context import Context


class World:

    def __init__(self):
        self.sprites = list()
        self.x = 0

    def update(self, context: Context):
        self.x = (self.x - (1 / 60) * context.speed * context.time_factor) % 2.0

        for sprite in self.sprites:
            sprite.render(context)

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

        for sprite in self.sprites:
            sprite.render(surface, size_factor)
