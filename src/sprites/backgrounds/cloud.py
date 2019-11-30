import random
from typing import Optional

from const import Const
from sprite import Type
from sprites.background import Background


class Cloud(Background):

    def __init__(self, x: Optional[float] = None, fullscreen: Optional[bool] = None):
        top = 0.8 if fullscreen is True else 0.5
        super().__init__(
            f"../res/img/cloud_{random.randint(1, 5)}.png",
            Const.game_height * (top * random.random() - 0.05),
            0.05 + 0.05 * random.random(),
            x
        )

    def type(self) -> Type:
        return Type.CLOUD

    def z_index(self) -> float:
        return self.speed
