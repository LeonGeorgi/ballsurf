from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

import pygame

from gamerect import GameRect
from src.context import Context


class Sprite(ABC):

    @abstractmethod
    def update(self, context: Context, sprites: Sprites):
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface, size_factor: float):
        pass

    @abstractmethod
    def box(self) -> GameRect:
        pass


class Sprites:
    def __init__(self, initial_sprites: List[Sprite]):
        self.sprite_list: List[Sprite] = initial_sprites

    def __iter__(self):
        return iter(self.sprite_list)
