from __future__ import annotations

import pygame


class GameRect:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def to_pygame(self, size_factor):
        return pygame.Rect(self.left * size_factor, self.top * size_factor, self.width * size_factor,
                           self.height * size_factor)

    def to_ellipse_data(self, size_factor):
        width = self.width * size_factor / 2
        height = self.height * size_factor / 2
        return int(self.left * size_factor + width), int(self.top * size_factor + height), int(width), int(height)

    def __str__(self):
        return f'GameRect(left={self.left}, top={self.top}, width={self.width}, height={self.height})'

    def intersects_with(self, other: GameRect) -> bool:
        return not (other.left > self.left + self.width or
                    other.left + other.width < self.left or
                    other.top > self.top + self.height or
                    other.top + other.height < self.top)
