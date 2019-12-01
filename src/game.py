from __future__ import annotations

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
from sprites.backgrounds.cloud import Cloud
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
        super().__init__("Ballsurf", [
            ("Start", self.start),
            ("Quit", self.quit)
        ])

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
            ("Retry", self.retry),
            ("Quit", self.quit)
        ])

        self.world = world

    def render(self, surface: pygame.Surface, size_factor: float):
        self.world.render(surface, size_factor)

        s = pygame.Surface((surface.get_width(), surface.get_height()))
        s.set_alpha(150)
        s.fill((0, 0, 0))
        surface.blit(s, (0, 0))

        super().render(surface, size_factor)

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
        context.running_time += context.time_factor / Const.fps
        context.meters += context.x_delta

        self.world.update(context)

        if context.lost:
            return GameStateLost(self.world)

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
