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
    tartan_height = 1.5
    tartan_top = game_height - tartan_height

    @staticmethod
    def tartan_area(surface: pygame.Surface) -> pygame.Rect:
        print(Const.tartan_top)
        return pygame.Rect(0, int(surface.get_height() * Const.tartan_top / Const.game_height),
                           surface.get_width(),
                           int(surface.get_height() * Const.tartan_height / Const.game_height) + 1)
