import random
from typing import Optional

from const import Const
from sprite import Type
from sprites import Background
from sprites import Hills


class Grass(Background):

    def __init__(self, hills: Hills, x: Optional[float] = None):
        super().__init__(
            f"res/img/grass_{random.randint(4, 6)}.png",
            0,
            0.3,
            x,
            False
        )

        min_y = max(hills.get_y_at(self.x), hills.get_y_at(self.x + self.width))
        self.y = (Const.tartan_top - min_y) * random.random() + min_y

    def type(self) -> Type:
        return Type.GRASS

    def z_index(self) -> float:
        return self.y + self.height
