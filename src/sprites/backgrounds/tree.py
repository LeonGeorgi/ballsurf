import random
from typing import Optional

from const import Const
from sprite import Type
from sprites.background import Background
from sprites.hills import Hills


class Tree(Background):

    def __init__(self, hills: Hills, x: Optional[float] = None):
        super().__init__(
            f"../res/img/tree_{random.randint(1, 2)}.png",
            0,
            0.3,
            x
        )

        min_y = hills.get_y_at(self.x + self.width / 2) + self.height * 0.2
        self.y = (Const.tartan_top - min_y) * random.random() + min_y - self.height

    def type(self) -> Type:
        return Type.TREE

    def z_index(self) -> float:
        return self.y + self.height
