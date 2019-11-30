from typing import Tuple

from sprites.ball import Ball


class BouncyBall(Ball):
    def diameter(self) -> float:
        return 0.7

    def bounciness(self) -> float:
        return 1.6

    def color(self) -> Tuple[int, int, int]:
        return 235, 68, 199


class DeadBall(Ball):
    def diameter(self) -> float:
        return 0.6

    def bounciness(self) -> float:
        return 0.35

    def color(self) -> Tuple[int, int, int]:
        return 150, 150, 150


class LargeBall(Ball):
    def diameter(self) -> float:
        return 1.1

    def bounciness(self) -> float:
        return 0.75

    def color(self) -> Tuple[int, int, int]:
        return 189, 111, 209


class RegularBall(Ball):
    def diameter(self) -> float:
        return 0.8

    def bounciness(self) -> float:
        return 1

    def color(self) -> Tuple[int, int, int]:
        return 26, 160, 237


class SmallBall(Ball):
    def diameter(self) -> float:
        return 0.5

    def bounciness(self) -> float:
        return 1.2

    def color(self) -> Tuple[int, int, int]:
        return 224, 124, 43
