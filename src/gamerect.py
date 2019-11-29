from __future__ import annotations

import pygame


class GameRect:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def to_pygame(self, size_factor):
        left = self.left * size_factor
        top = self.top * size_factor
        left_width = min(left, 0)
        top_height = min(top, 0)
        left = max(left, 0)
        top = max(top, 0)

        return pygame.Rect(left, top, self.width * size_factor + left_width,
                           self.height * size_factor + top_height)

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
