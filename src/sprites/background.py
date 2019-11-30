from typing import Optional

import pygame

from const import Const
from context import Context
from gamerect import GameRect
from sprite import Sprite, Sprites


class Background(Sprite):

    def __init__(self, filename: str, top: float, height: float, speed: float, x: Optional[float] = None):
        if x is None:
            x = 2

        self.x = x * Const.game_height
        self.speed = speed

        self.image = pygame.image.load(filename)
        self.y = top
        self.height = height
        self.width = self.image.get_width() / self.image.get_height() * self.height

    def update(self, context: Context, sprites: Sprites):
        self.x -= context.x_delta * self.speed

    def render(self, surface: pygame.Surface, size_factor: float):
        w = int(self.width * size_factor)
        h = int(self.height * size_factor)
        img = pygame.transform.smoothscale(self.image, (w, h))

        l = int(self.x * size_factor)
        rect = pygame.Rect(0 if l >= 0 else abs(l), 0, w + min(0, l), h)

        surface.blit(img, (max(0, l), self.y * size_factor), rect)

    @property
    def box(self) -> GameRect:
        return GameRect(self.x, self.y, self.width, self.height)

    def can_delete(self) -> bool:
        return self.x <= -self.height
