from __future__ import annotations

import sys
import time
from abc import ABC, abstractmethod
from typing import List, Callable, Optional, Tuple

import pygame
import pygame.font

from context import Context, Key
from world import World

DELTA_FACTOR = 1 / 60
MIN_BUTTON_TIME_DELTA = 0.2


class GameState(ABC):

    @abstractmethod
    def update(self, context: Context) -> Optional[GameState]:
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface, size_factor: float):
        pass


class GameMenu(GameState):
    PADDING = 10

    def __init__(self, name: str, entries: List[Tuple[str, Callable[[], Optional[GameState]]]]):
        self.name = name
        self.entries = entries
        self.index = 0
        self.last_button = time.time()

    def update(self, context: Context) -> Optional[GameState]:
        if Key.QUIT in context.key_strokes:
            return None

        t = time.time()
        if t - self.last_button < MIN_BUTTON_TIME_DELTA:
            return self

        if Key.ACCEPT in context.key_strokes:
            self.last_button = t
            _, callback = self.entries[self.index]
            return callback()

        if Key.DOWN in context.key_strokes:
            self.last_button = t
            self.index = (self.index + 1) % len(self.entries)
        elif Key.UP in context.key_strokes:
            self.last_button = t
            self.index -= 1
            if self.index < 0:
                self.index = len(self.entries) - 1

        return self

    def render(self, surface: pygame.Surface, size_factor: float):
        surface_width = surface.get_width()
        surface_height = surface.get_height()

        font = pygame.font.Font("../res/Game_font.ttf", surface_height // 10)
        entries = [(font.render(text, True, (255, 255, 255)), callback) for text, callback in self.entries]
        width = max(x.get_width() for x, _ in entries) + 2 * GameMenu.PADDING
        height = max(x.get_height() for x, _ in entries) + 2 * GameMenu.PADDING

        left = surface_width // 2 - (width // 2)
        top = surface_height // 2 - (height * (len(self.entries) + 1.5) // 2)

        header = font.render(self.name, True, (255, 255, 255))
        header_left = surface_width // 2 - header.get_width() // 2
        surface.blit(header, (header_left, top))
        top += int(height * 1.5)

        index = 0
        for img, _ in entries:
            if self.index == index:
                surface.fill((50, 50, 50),
                             pygame.Rect(left, top + index * height, width,
                                         height))

            width_center = width // 2 - img.get_width() // 2
            surface.blit(img, (left + width_center, top + index * height + GameMenu.PADDING))
            index += 1


class GameStateMenu(GameMenu):

    def __init__(self):
        super().__init__("Ballsurf", [
            ("Start", self.start),
            ("Quit", self.quit)
        ])

    @staticmethod
    def start() -> Optional[GameState]:
        return GameStateRunning()

    @staticmethod
    def quit() -> Optional[GameState]:
        return None


class GameStatePause(GameMenu):

    def __init__(self, running: GameStateRunning):
        super().__init__("Pause", [
            ("Resume", self.resume),
            ("Quit", self.quit)
        ])

        self.running = running

    def resume(self) -> Optional[GameState]:
        return self.running

    @staticmethod
    def quit() -> Optional[GameState]:
        return None


class GameStateLost(GameMenu):

    def __init__(self):
        super().__init__("Game over", [
            ("Retry", self.retry),
            ("Quit", self.quit)
        ])

    @staticmethod
    def retry() -> Optional[GameState]:
        return GameStateRunning()

    @staticmethod
    def quit() -> Optional[GameState]:
        return None


class GameStateRunning(GameState):

    def __init__(self):
        self.world = World()
        self.first = True

    def update(self, context: Context) -> GameState:
        if self.first:
            context.reset()
            self.first = False

        if Key.ESCAPE in context.key_strokes:
            return GameStatePause(self)

        context.current_speed += ((context.desired_speed * 2) - context.current_speed) * 0.003
        context.desired_speed += context.desired_speed_increase * context.time_factor
        context.x_delta = DELTA_FACTOR * context.current_speed * context.time_factor

        self.world.update(context)

        if context.lost:
            return GameStateLost()

        return self

    def render(self, surface: pygame.Surface, size_factor: float):
        self.world.render(surface, size_factor)


class Game:
    def __init__(self):
        self.game_state = GameStateMenu()

    def update(self, context: Context):
        self.game_state = self.game_state.update(context)

        if self.game_state is None:
            pygame.quit()
            sys.exit()

    def render(self, surface: pygame.Surface, size_factor: float):
        self.game_state.render(surface, size_factor)
