from typing import Dict, Tuple

import pygame


class Cache:
    def __init__(self, filename, mirrored):
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.flip(self.image, mirrored, False)
        self.sizes: Dict[Tuple[int, int], pygame.Surface] = {}

    def scale(self, width: int, height: int) -> pygame.Surface:
        key = (width, height)
        if key not in self.sizes:
            img = pygame.transform.scale(self.image, (width, height))
            self.sizes[key] = img

        return self.sizes[key]

    def clear(self):
        self.sizes = {}


class CachedImage:
    cache: Dict[Tuple[str, bool], Cache] = {}

    def __init__(self, filename: str, mirrored: bool = False):
        self.filename = filename
        self.mirrored = mirrored

        self.key = (filename, mirrored)
        if self.key not in CachedImage.cache:
            CachedImage.cache[self.key] = Cache(filename, mirrored)

    @property
    def original(self) -> pygame.Surface:
        return CachedImage.cache[self.key].image

    def get_width(self) -> int:
        return self.original.get_width()

    def get_height(self) -> int:
        return self.original.get_height()

    def scale(self, width: int, height: int):
        return CachedImage.cache[self.key].scale(width, height)

    @staticmethod
    def clear_cache():
        for cache in CachedImage.cache.values():
            cache.clear()
