from __future__ import annotations

from abc import ABC, abstractmethod
from enum import IntEnum

import pygame

from context import Context
from gamerect import GameRect


class Type(IntEnum):
    PLAYER = 0
    BALL = 1
    BACKGROUND = 2


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


class Sprites(list):

    def __init__(self, l):
        super().__init__(l)

    def get_balls(self):
        for x in self:
            if x.type() is Type.BALL:
                yield x
