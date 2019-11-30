from typing import Tuple

from sprites.ball import Ball


class RegularBall(Ball):
    def diameter(self) -> float:
        return 1

    def bounciness(self) -> float:
        return 1

    def color(self) -> Tuple[int, int, int]:
        return 26, 160, 237
