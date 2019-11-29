import pygame

from src.context import Context


class World:

    def __init__(self):
        self.sprites = list()

    def update(self, context: Context):
        pass

    def render(self, surface: pygame.Surface):
        pass
