import pygame


class Const:
    # game height in meters
    game_height = 8
    fps = 60
    countdown = 3

    @staticmethod
    def tartan_area(surface: pygame.Surface) -> pygame.Rect:
        return pygame.Rect(0, surface.get_height() * (Const.game_height - 1.5) // Const.game_height,
                           surface.get_width(),
                           surface.get_height() * (1 - (Const.game_height - 1.5) // Const.game_height))
