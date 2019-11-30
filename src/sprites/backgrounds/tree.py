import random
from typing import Optional

from const import Const
from sprite import Type
from sprites.background import Background


class Tree(Background):

    def __init__(self, x: Optional[float] = None):
        h = 2.0
        super().__init__(
            f"../res/img/tree.png",
            Const.game_height * (0.25 * random.random() + 0.65) - h,
            h,
            0.5,
            x
        )

    def type(self) -> Type:
        return Type.TREE

    def z_index(self) -> float:
        return self.y
