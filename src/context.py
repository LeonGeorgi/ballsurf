from enum import IntEnum
from typing import Set


class Key(IntEnum):
    MAIN = 0,
    ACCEPT = 1,
    UP = 2,
    DOWN = 3,
    ESCAPE = 4,
    QUIT = 5


class Context:

    def __init__(self):
        self.reset()

        self.time_factor = 1.0
        self.key_strokes: Set[Key] = set()
        self.x_delta = 0.0

    # noinspection PyAttributeOutsideInit
    def reset(self):
        self.current_speed = 2.0
        self.desired_speed = 2.0
        self.desired_speed_increase = 0.0001
        self.gravity = 9.81
        self.speed_increase = 0.005
        self.speed_factor_dec = 0.9
        self.lost = False
