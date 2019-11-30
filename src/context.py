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
        self.current_speed = 1.0
        self.desired_speed = 1.0
        self.desired_speed_increase = 0.0001
        self.gravity = 0.00003
        self.speed_increase = 0.005
        self.speed_factor_dec = 0.9
        self.lost = False

        self.time_factor = 1.0
        self.key_strokes: Set[Key] = set()
        self.x_delta = 0.0

    def reset(self):
        self.current_speed = 1.0
        self.desired_speed = 1.0
        self.desired_speed_increase = 0.0001
        self.gravity = 0.00003
        self.speed_increase = 0.005
        self.speed_factor_dec = 0.9
        self.lost = False
