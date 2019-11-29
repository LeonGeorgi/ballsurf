from enum import Enum
from typing import Set


class Key(Enum):
    MAIN = 0


class Context:

    def __init__(self):
        self.speed = 1.0
        self.time_factor = 1.0
        self.key_strokes: Set[Key] = set()
