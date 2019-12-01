from enum import IntEnum
from typing import Set

from const import Const


class Key(IntEnum):
    ACTION = 0,
    NEXT = 2,
    PREV = 3,
    ESCAPE = 4,
    QUIT = 5,
    BACKSPACE = 6


class Context:

    def __init__(self):
        self.reset()

        self.time_factor = 1.0
        self.key_strokes: Set[Key] = set()
        self.x_delta = 0.0
        self.resize = False
        self.letter = ''

    # noinspection PyAttributeOutsideInit
    def reset(self):
        self.current_speed = Const.start_speed
        self.desired_speed = Const.start_speed
        self.desired_speed_increase = 0.0001
        self.bounciness_factor = 0.6

        self.gravity = 9.81
        self.speed_increase = Const.speed_increase
        self.speed_factor_dec = 0.9
        self.lost = False
        self.running_time = 0.0
        self.meters = Const.offset_meters
