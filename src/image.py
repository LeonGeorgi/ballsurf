from typing import Dict, Tuple

import pygame


class Cache:
    def __init__(self, filename):
        self.filename = filename
        self.image = pygame.image.load(filename)
        self.sizes: Dict[Tuple[int, int], pygame.Surface] = {}

    def scale(self, width: int, height: int) -> pygame.Surface:
        key = (width, height)
        if key not in self.sizes:
            img = pygame.transform.scale(self.image, (width, height))
            self.sizes[key] = img

        return self.sizes[key]


class CachedImage:
    cache: Dict[str, Cache] = {}

    def __init__(self, filename: str):
        self.filename = filename
        if filename not in CachedImage.cache:
            CachedImage.cache[filename] = Cache(filename)

    @property
    def original(self) -> pygame.Surface:
        return CachedImage.cache[self.filename].image

    def get_width(self) -> int:
        return self.original.get_width()

    def get_height(self) -> int:
        return self.original.get_height()

    def scale(self, width: int, height: int):
        return CachedImage.cache[self.filename].scale(width, height)
