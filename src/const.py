import pygame


class Const:
    # game height in meters
    game_height = 8
    fps = 60
    pixel_size = 0.05
    speed_increase = 0.005
    player_position = game_height * 0.2
    start_speed = 4.0
    offset_meters = start_speed * -3

    @staticmethod
    def tartan_area(surface: pygame.Surface) -> pygame.Rect:
        return pygame.Rect(0, surface.get_height() * (Const.game_height - 1.5) // Const.game_height,
                           surface.get_width(),
                           surface.get_height() * (1 - (Const.game_height - 1.5) // Const.game_height))
