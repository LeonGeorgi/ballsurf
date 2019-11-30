from typing import Tuple

from sprites.ball import Ball


class SmallBall(Ball):
    def diameter(self) -> float:
        return 0.5

    def bounciness(self) -> float:
        return 2

    def color(self) -> Tuple[int, int, int]:
        return 224, 124, 43
