import random
from typing import Optional

from const import Const
from sprite import Type
from sprites.background import Background


class Tree(Background):

    def __init__(self, x: Optional[float] = None):
        super().__init__(
            f"../res/img/tree_{random.randint(1, 2)}.png",
            Const.game_height * (0.2 * random.random() + 0.35),
            0.3,
            x
        )

    def type(self) -> Type:
        return Type.TREE

    def z_index(self) -> float:
        return self.y
