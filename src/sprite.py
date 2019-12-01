from __future__ import annotations

from abc import ABC, abstractmethod
from enum import IntEnum

import pygame

from context import Context
from gamerect import GameRect


class Type(IntEnum):
    CLOUD = 0
    HILLS = 1
    GRASS = 2
    TREE = 3
    TARTAN = 4
    BALL = 5
    PLAYER = 6


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

    @abstractmethod
    def type(self) -> Type:
        pass

    def can_delete(self) -> bool:
        return False

    def z_index(self) -> float:
        return 0.0


class Sprites(list):

    def __init__(self, l):
        super().__init__(l)

    def get(self, type: Type):
        for x in self:
            if x.type() is type:
                yield x
