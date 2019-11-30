import random
from typing import Optional

from const import Const
from sprite import Type
from sprites.background import Background


class Cloud(Background):

    def __init__(self, x: Optional[float] = None):
        super().__init__(
            f"../res/img/cloud_{random.randint(1, 5)}.png",
            Const.game_height * (0.5 * random.random() - 0.05),
            0.2 + 0.06 * random.random(),
            x
        )

    def type(self) -> Type:
        return Type.CLOUD

    def z_index(self) -> float:
        return self.speed
