from enum import IntEnum
from typing import Set

from pygame.mixer import Sound

from const import Const


class Key(IntEnum):
    ENTER = 0,
    SPACE = 1,
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
        self.damage_sound = Sound("res/sounds/damage.ogg")

    # noinspection PyAttributeOutsideInit
    def reset(self):
        self.current_speed = Const.start_speed
        self.desired_speed = Const.start_speed
        self.desired_speed_increase = Const.desired_speed_increase
        self.bounciness_factor = Const.bounciness_factor

        self.gravity = Const.gravity
        self.speed_increase = Const.speed_increase
        self.speed_factor_dec = 0.9
        self.lost = False
        self.running_time = 0.0
        self.meters = Const.offset_meters
