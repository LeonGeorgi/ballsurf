import random
from typing import Optional

import pygame

from const import Const
from context import Context
from gamerect import GameRect
from image import CachedImage
from sprite import Sprite, Sprites


class Background(Sprite):

    def __init__(self, filename: str, top: float, speed: float, x: Optional[float] = None):
        if x is None:
            x = 2

        self.x = x * Const.game_height
        self.speed = speed

        self.image = CachedImage(filename, random.getrandbits(1))

        self.height = self.image.get_height() * Const.pixel_size
        self.width = self.image.get_width() * Const.pixel_size
        self.y = top

    def update(self, context: Context, sprites: Sprites):
        self.x -= context.x_delta * self.speed

    def render(self, surface: pygame.Surface, size_factor: float):
        h = int(self.height * size_factor)
        w = int(self.width * size_factor)

        img = self.image.scale(w, h)

        l = int(self.x * size_factor)
        rect = pygame.Rect(0 if l >= 0 else abs(l), 0, w + min(0, l), h)

        surface.blit(img, (max(0, l), self.y * size_factor), rect)

    @property
    def box(self) -> GameRect:
        return GameRect(self.x, self.y, self.width, self.height)

    def can_delete(self) -> bool:
        return self.x <= -self.width
