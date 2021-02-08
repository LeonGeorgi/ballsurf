import math
import random

import pygame

import utils
from const import Const
from context import Context
from sprite import Sprites, Type
from sprites import Hills, Nicholas, Tartan
from sprites.backgrounds import Cloud, Grass, Tree
from sprites.balls import *


class World:
    def __init__(self):
        self.hills = Hills()
        self.sprites = Sprites([Nicholas(), self.hills, Tartan()])
        self.x = 0
        self.meters = 0
        self.running_time = 0

        self.last_background = None
        self.last_size = None
        self.last_ball_x = self.meters
        self.next_ball_distance = 1
        self.next_ball = RegularBall
        self.ball_stats = {
            RegularBall: (100, 9 / 16),
            SmallBall: (7, 10 / 16),
            LargeBall: (7, 7 / 16),
            BouncyBall: (5, 12 / 16),
            DeadBall: (3, 2 / 16),
            BoostBall: (5, 12 / 16)
        }

        for i in range(8):
            self.sprites.append(Cloud(3 * random.random() - 0.5))

        for i in range(45):
            self.sprites.append(Grass(self.hills, 3 * random.random() - 0.5))

        for i in range(10):
            self.sprites.append(Tree(self.hills, 3 * random.random() - 0.5))

        balls = []
        for i in range(10):
            new = random.choices([RegularBall, SmallBall, LargeBall, BouncyBall, DeadBall, BoostBall],
                                 [100, 7, 7, 5, 3, 3])
            ball = new[0](Const.game_height * 1.5 * random.random() - 1)
            if not any(b.box.intersects_with(ball.box) for b in balls):
                balls.append(ball)
                self.sprites.append(ball)

    def __update_clouds(self):
        clouds = list(self.sprites.get(Type.CLOUD))

        if len(clouds) < 10 and random.random() < 0.02:
            cloud = Cloud()
            if not any(c.box.intersects_with(cloud.box) for c in clouds):
                self.sprites.append(cloud)

    def __update_grass(self):
        grasses = list(self.sprites.get(Type.GRASS))

        if len(grasses) < 100 and random.random() < 0.1:
            tree = Grass(self.hills)
            if not any(c.box.intersects_with(tree.box) for c in grasses):
                self.sprites.append(tree)

    def __update_trees(self):
        trees = list(self.sprites.get(Type.TREE))

        if len(trees) < 30 and random.random() < 0.03:
            tree = Tree(self.hills)
            if not any(c.box.intersects_with(tree.box) for c in trees):
                self.sprites.append(tree)

    def __update_balls(self, context: Context):
        distance_to_right = (self.meters + Const.game_height / 9 * 16) - self.last_ball_x
        v = context.desired_speed * 1.5
        a = context.gravity
        h = Const.game_height
        s_n = v * 2 * math.sqrt(2) * math.sqrt(h / a)
        if distance_to_right >= self.next_ball_distance:
            new_ball_x = self.last_ball_x + self.next_ball_distance
            self.sprites.append(self.next_ball(new_ball_x - self.meters))
            self.last_ball_x = new_ball_x
            next_mu = self.ball_stats[self.next_ball][1] * s_n / 2

            h = min(max(2, random.gauss(next_mu, (next_mu / 2))), s_n)
            self.next_ball_distance += 0.4
            if self.meters >= -8 or h < self.next_ball_distance:
                self.next_ball_distance = h

            self.next_ball = random.choices(*(list(a) for a in
                                              zip(*list((ball, stats[0]) for ball, stats in
                                                        self.ball_stats.items()))))[0]

    def update(self, context: Context):
        self.meters = context.meters
        self.running_time = context.running_time

        del_sprites = []
        for sprite in self.sprites:
            if sprite.can_delete():
                del_sprites.append(sprite)

        for sprite in del_sprites:
            self.sprites.remove(sprite)

        self.__update_clouds()
        self.__update_grass()
        self.__update_trees()
        self.__update_balls(context)

        for sprite in self.sprites:
            sprite.update(context, self.sprites)

    def render(self, surface: pygame.Surface, size_factor: float):
        size = surface.get_size()
        if size != self.last_size:
            self.last_background = utils.vertical_gradient(size, (75, 142, 188, 255), (94, 178, 235, 255))
            self.last_size = size
        surface.blit(self.last_background, (0, 0))

        self.sprites.sort(key=lambda x: (x.type().value, x.z_index()))
        for sprite in self.sprites:
            sprite.render(surface, size_factor)

        if int(self.meters) < 0:
            t = (Const.offset_meters * self.running_time) / (Const.offset_meters - self.meters)

            font = pygame.font.Font("res/arcade.ttf", surface.get_height() // 5)
            img = font.render(str(int(t - self.running_time) + 1), True, (0, 0, 0))
            surface.blit(img, (
                surface.get_width() // 2 - img.get_width() // 2,
                surface.get_height() // 2 - img.get_height() // 2
            ))
        else:
            font = pygame.font.Font("res/arcade.ttf", surface.get_height() // 10)
            img = font.render(str(int(self.meters)), True, (0, 0, 0))
            surface.blit(img, (int(surface.get_width() * 0.95) - img.get_width(), int(surface.get_height() * 0.05)))
