from sprites.ball import Ball


class BouncyBall(Ball):

    def filename(self) -> str:
        return "../res/img/ball_bouncy.png"

    def bounciness(self) -> float:
        return 1.6


class DeadBall(Ball):
    def filename(self) -> str:
        return "../res/img/ball_dead.png"

    def bounciness(self) -> float:
        return 0.35


class LargeBall(Ball):
    def filename(self) -> str:
        return "../res/img/ball_large.png"

    def bounciness(self) -> float:
        return 0.75


class RegularBall(Ball):
    def filename(self) -> str:
        return "../res/img/ball_regular.png"

    def bounciness(self) -> float:
        return 1


class SmallBall(Ball):
    def filename(self) -> str:
        return "../res/img/ball_small.png"

    def bounciness(self) -> float:
        return 1.2
