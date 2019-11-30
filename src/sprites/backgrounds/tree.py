import random
from typing import Optional

from const import Const
from sprite import Type
from sprites.background import Background


class Tree(Background):

    def __init__(self, x: Optional[float] = None):
        top = Const.game_height * (0.2 * random.random() + 0.62)
        h = (top / Const.game_height - 0.62) * 1.5 / 0.25 + 1
        top -= h + 0.1
        super().__init__(
            f"../res/img/tree.png",
            top,
            h,
            0.5,
            x
        )

    def type(self) -> Type:
        return Type.TREE

    def z_index(self) -> float:
        return self.y
