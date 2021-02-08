from sprites import Ball


class BouncyBall(Ball):

    def immediate_speed_increase(self) -> float:
        return 2.5

    def desired_speed_increase(self) -> float:
        return 0

    def filename(self) -> str:
        return "res/img/ball_bouncy.png"

    def bounciness(self) -> float:
        return 1.6


class BoostBall(Ball):
    def immediate_speed_increase(self) -> float:
        return 2

    def desired_speed_increase(self) -> float:
        return 1

    def filename(self) -> str:
        return "res/img/ball_boost.png"

    def bounciness(self) -> float:
        return 1.6


class DeadBall(Ball):
    def immediate_speed_increase(self) -> float:
        return -1

    def desired_speed_increase(self) -> float:
        return 0

    def filename(self) -> str:
        return "res/img/ball_dead.png"

    def bounciness(self) -> float:
        return 0.35


class LargeBall(Ball):
    def immediate_speed_increase(self) -> float:
        return 0.5

    def desired_speed_increase(self) -> float:
        return 0

    def filename(self) -> str:
        return "res/img/ball_large.png"

    def bounciness(self) -> float:
        return 0.75


class RegularBall(Ball):
    def immediate_speed_increase(self) -> float:
        return 1

    def desired_speed_increase(self) -> float:
        return 0

    def filename(self) -> str:
        return "res/img/ball_regular.png"

    def bounciness(self) -> float:
        return 1


class SmallBall(Ball):
    def immediate_speed_increase(self) -> float:
        return 1.5

    def desired_speed_increase(self) -> float:
        return 0

    def filename(self) -> str:
        return "res/img/ball_small.png"

    def bounciness(self) -> float:
        return 1.2
