from __future__ import annotations

import json
import os
import random
import sys
import time
from abc import ABC, abstractmethod
from typing import List, Callable, Optional, Tuple

import pygame
import pygame.font

import utils
from const import Const
from context import Context, Key
from sprite import Sprites, Type
from sprites.backgrounds import Cloud
from world import World

DELTA_FACTOR = 1 / 60
MIN_BUTTON_TIME_DELTA = 0.2


class GameState(ABC):

    def __init__(self):
        self.should_ignore_keys = True

    @abstractmethod
    def update(self, context: Context) -> Optional[GameState]:
        if len(context.key_strokes) == 0:
            self.should_ignore_keys = False
        if self.should_ignore_keys:
            context.key_strokes = set()

        return self

    @abstractmethod
    def render(self, surface: pygame.Surface, size_factor: float):
        pass


class GameMenu(GameState):
    PADDING = 10

    def __init__(self, name: str, entries: List[Tuple[str, Callable[[], Optional[GameState]]]]):
        super().__init__()
        self.name = name
        self.entries = entries
        self.index = 0
        self.last_button = time.time()

    def update(self, context: Context) -> Optional[GameState]:
        super().update(context
                       )
        if Key.QUIT in context.key_strokes:
            return None

        if len(context.key_strokes) == 0:
            self.last_button = 0

        t = time.time()
        if t - self.last_button < MIN_BUTTON_TIME_DELTA:
            return self

        if Key.ACTION in context.key_strokes:
            self.last_button = t
            _, callback = self.entries[self.index]
            return callback()

        if Key.NEXT in context.key_strokes:
            self.last_button = t
            self.index = (self.index + 1) % len(self.entries)
        elif Key.PREV in context.key_strokes:
            self.last_button = t
            self.index -= 1
            if self.index < 0:
                self.index = len(self.entries) - 1

        return self

    def render(self, surface: pygame.Surface, size_factor: float):
        surface_width = surface.get_width()
        surface_height = surface.get_height()

        font = pygame.font.Font("../res/arcade.ttf", surface_height // 10)
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
                s = pygame.Surface((width - GameMenu.PADDING, height))
                s.set_alpha(70)
                s.fill((255, 255, 255))
                surface.blit(s, (left, top + index * height))

            width_center = width // 2 - img.get_width() // 2
            surface.blit(img, (left + width_center, top + index * height + GameMenu.PADDING))
            index += 1


class GameStateMenu(GameMenu):

    def __init__(self):
        items = [
            ("Start", self.start),
            ("Quit", self.quit)
        ]

        if len(GameStateHighScore.load_score()) > 0:
            items.insert(1, ("Score", self.score))

        super().__init__("Ballsurf", items)

        self.sprites = Sprites([])
        self.first = True

        for i in range(8):
            self.sprites.append(Cloud(3 * random.random() - 0.5, True))

        self.last_background = None
        self.last_size = None

    def __update_clouds(self):
        del_sprites = []
        for sprite in self.sprites:
            if sprite.can_delete():
                del_sprites.append(sprite)

        for sprite in del_sprites:
            self.sprites.remove(sprite)

        clouds = list(self.sprites.get(Type.CLOUD))

        if len(clouds) < 10 and random.random() < 0.02:
            cloud = Cloud(None, True)
            if not any(c.box.intersects_with(cloud.box) for c in clouds):
                self.sprites.append(cloud)

    def update(self, context: Context) -> Optional[GameState]:
        if self.first:
            context.reset()
            self.first = False

        context.current_speed += ((context.desired_speed * 2) - context.current_speed) * 0.003
        context.desired_speed += context.desired_speed_increase * context.time_factor
        context.x_delta = DELTA_FACTOR * context.current_speed * context.time_factor
        context.running_time += context.time_factor / Const.fps
        context.meters += context.x_delta

        self.__update_clouds()

        for sprite in self.sprites:
            sprite.update(context, self.sprites)

        return super().update(context)

    def render(self, surface: pygame.Surface, size_factor: float):
        size = surface.get_size()
        if size != self.last_size:
            self.last_background = utils.vertical_gradient(size, (75, 142, 188, 255), (94, 178, 235, 255))
            self.last_size = size
        surface.blit(self.last_background, (0, 0))

        self.sprites.sort(key=lambda x: (x.type().value, x.z_index()))
        for sprite in self.sprites:
            sprite.render(surface, size_factor)

        s = pygame.Surface((surface.get_width(), surface.get_height()))
        s.set_alpha(150)
        s.fill((0, 0, 0))
        surface.blit(s, (0, 0))

        super().render(surface, size_factor)

    @staticmethod
    def start() -> Optional[GameState]:
        return GameStateRunning()

    def score(self) -> Optional[GameState]:
        return GameStateHighScore(self)

    @staticmethod
    def quit() -> Optional[GameState]:
        return None


class GameStatePause(GameMenu):

    def __init__(self, running: GameStateRunning):
        super().__init__("Pause", [
            ("Resume", self.resume),
            ("Restart", self.restart),
            ("Quit", self.quit)
        ])

        self.running = running

    def render(self, surface: pygame.Surface, size_factor: float):
        self.running.world.render(surface, size_factor)

        s = pygame.Surface((surface.get_width(), surface.get_height()))
        s.set_alpha(150)
        s.fill((0, 0, 0))
        surface.blit(s, (0, 0))

        super().render(surface, size_factor)

    def resume(self) -> Optional[GameState]:
        return self.running

    @staticmethod
    def restart() -> Optional[GameState]:
        return GameStateRunning()

    @staticmethod
    def quit() -> Optional[GameState]:
        return None


class GameStateLost(GameMenu):

    def __init__(self, world: World):
        super().__init__("Game over", [
            ("Next", self.next),
            ("Quit", self.quit)
        ])

        self.world = world
        self.first = True
        self.close = False

    def update(self, context: Context) -> Optional[GameState]:
        if self.close:
            return GameStateRunning()

        return super().update(context)

    def render(self, surface: pygame.Surface, size_factor: float):
        self.world.render(surface, size_factor)

        s = pygame.Surface((surface.get_width(), surface.get_height()))
        s.set_alpha(150)
        s.fill((0, 0, 0))
        surface.blit(s, (0, 0))

        super().render(surface, size_factor)

    def next(self) -> Optional[GameState]:
        score = int(self.world.meters)

        if GameStateHighScore.is_record(score) and self.first:
            self.first = False
            return GameStateHighScore(self, score)

        return GameStateRunning()

    @staticmethod
    def quit() -> Optional[GameState]:
        return None


class GameStateRunning(GameState):

    def __init__(self):
        super().__init__()
        self.world = World()
        self.first = True

    def update(self, context: Context) -> GameState:
        super().update(context)

        if self.first:
            context.reset()
            self.first = False

        if Key.ESCAPE in context.key_strokes:
            return GameStatePause(self)

        context.current_speed += ((context.desired_speed * 2) - context.current_speed) * 0.003
        context.desired_speed += context.desired_speed_increase * context.time_factor
        context.x_delta = DELTA_FACTOR * context.current_speed * context.time_factor
        context.running_time += context.time_factor / Const.fps
        context.meters += context.x_delta

        self.world.update(context)

        if context.lost:
            return GameStateLost(self.world)

        return self

    def render(self, surface: pygame.Surface, size_factor: float):
        self.world.render(surface, size_factor)


class GameStateHighScore(GameState):
    filename = "ballsurf.json"

    def __init__(self, previous_state: GameState, score: Optional[int] = None):
        super().__init__()
        self.previous_state = previous_state
        self.score = score
        self.name = ""
        self.index = -1
        self.not_blocking = False

        self.high_score: List[Tuple[str, int]] = GameStateHighScore.load_score()

        if score is not None:
            for i in range(len(self.high_score)):
                if score > self.high_score[i][1]:
                    self.index = i
                    self.high_score.insert(i, (self.name, score))
                    break

            if len(self.high_score) < 5:
                self.index = len(self.high_score)
                self.high_score.append((self.name, score))

        self.high_score = self.high_score[:5]

    @staticmethod
    def load_score() -> List[Tuple[str, int]]:
        high_score = []
        if os.path.isfile(GameStateHighScore.filename):
            with open(GameStateHighScore.filename, 'r') as file:
                high_score = json.load(file)

        high_score = high_score[:5]

        return high_score

    @staticmethod
    def is_record(score) -> bool:
        scores = GameStateHighScore.load_score()

        if len(scores) < 5:
            return True

        for _, s in scores:
            if score > s:
                return True

        return False

    def save(self):
        with open(GameStateHighScore.filename, 'w') as file:
            json.dump(self.high_score, file)

    def update(self, context: Context) -> Optional[GameState]:
        super().update(context)

        if Key.ESCAPE in context.key_strokes or Key.ACTION in context.key_strokes and self.score is None and not self.not_blocking:
            self.previous_state.close = True
            return self.previous_state

        if Key.ACTION in context.key_strokes and self.score is not None:
            self.save()
            self.score = None
            self.not_blocking = True

        if Key.ACTION not in context.key_strokes:
            self.not_blocking = False

        if self.index >= 0 and self.score is not None and context.letter.isprintable():
            self.name += context.letter
            if len(self.name) >= 10:
                self.name = self.name[:10]
            self.high_score[self.index] = (self.name, self.score)

        if Key.BACKSPACE in context.key_strokes and self.score is not None and len(self.name) > 0:
            self.name = self.name[:-1]
            self.high_score[self.index] = (self.name, self.score)

        context.key_strokes = set()

        self.previous_state.update(context)

        return self

    def render(self, surface: pygame.Surface, size_factor: float):
        self.previous_state.render(surface, size_factor)

        s = pygame.Surface((surface.get_width(), surface.get_height()))
        s.set_alpha(150)
        s.fill((0, 0, 0))
        surface.blit(s, (0, 0))

        surface_width = surface.get_width()
        surface_height = surface.get_height()

        font = pygame.font.Font("../res/arcade.ttf", surface_height // 10)
        entries = [(font.render(text, True, (255, 255, 255)), font.render(str(score), True, (255, 255, 255))) for
                   text, score in self.high_score]

        height = max(x.get_height() for x, _ in entries) + 2 * GameMenu.PADDING

        left = int(surface_width * 0.25)
        right = int(surface_width * 0.75)

        top = surface_height // 2 - (height * (len(self.high_score) + 1.5) // 2)

        header = font.render("High score", True, (255, 255, 255))
        header_left = surface_width // 2 - header.get_width() // 2
        surface.blit(header, (header_left, top))
        top += int(height * 1.5)

        index = 0
        for text, score in entries:
            if self.index == index:
                s = pygame.Surface((surface_width // 2 + GameMenu.PADDING * 2, height))
                s.set_alpha(70)
                s.fill((255, 255, 255))
                surface.blit(s, (left - GameMenu.PADDING, top + index * height))

            surface.blit(text, (left, top + index * height + GameMenu.PADDING))
            surface.blit(score, (right - score.get_width(), top + index * height + GameMenu.PADDING))

            t = time.time()
            if self.index == index and self.score is not None and t - int(t) < 0.5:
                surface.fill((255, 255, 255), pygame.Rect(
                    left + text.get_width(),
                    top + index * height,
                    size_factor * Const.pixel_size,
                    height
                ))

            index += 1


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
