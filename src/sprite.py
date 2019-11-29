from abc import ABC, abstractmethod

import pygame

from src.world import World
from src.context import Context


class Sprite(ABC):

    @abstractmethod
    def update(self, context: Context, world: World):
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface, size_factor: float):
        pass

    @abstractmethod
    @property
    def box(self) -> pygame.Rect:
        pass
