import random
from typing import Optional

import pygame

from const import Const
from sprite import Type
from sprites.background import Background


class Tree(Background):

    def __init__(self, x: Optional[float] = None):
        super().__init__(
            f"../res/img/tree.png",
            Const.game_height * (0.2 * random.random() + 0.62),
            0.5,
            x
        )

    def render(self, surface: pygame.Surface, size_factor: float):
        return

    def type(self) -> Type:
        return Type.TREE

    def z_index(self) -> float:
        return self.y
