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

    def __str__(self):
        return f'GameRect(left={self.left}, top={self.top}, width={self.width}, height={self.height})'
