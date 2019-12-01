import pygame


class Const:
    # game height in meters
    game_height = 8
    fps = 60
    pixel_size = 0.05
    speed_increase = 0.005
    desired_speed_increase = 0.0001
    gravity = 9.81
    bounciness_factor = 0.6
    player_position = game_height * 0.2
    max_speed_increase = 3
    start_speed = 4.0
    offset_meters = start_speed * -3
    tartan_height = 1.5
    tartan_top = game_height - tartan_height

    @staticmethod
    def tartan_area(surface: pygame.Surface) -> pygame.Rect:
        return pygame.Rect(0, int(surface.get_height() * Const.tartan_top / Const.game_height),
                           surface.get_width(),
                           int(surface.get_height() * Const.tartan_height / Const.game_height) + 1)
