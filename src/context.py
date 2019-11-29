from enum import IntEnum
from typing import Set


class Key(IntEnum):
    MAIN = 0


class Context:

    def __init__(self):
        self.speed = 0.0
        self.gravity = 0.0001
        self.time_factor = 1.0
        self.key_strokes: Set[Key] = set()
        self.x_delta = 0.0
