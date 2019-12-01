import random

import pygame

import utils
from context import Context
from sprite import Sprites, Type
from sprites.backgrounds.cloud import Cloud
from sprites.backgrounds.tree import Tree
from sprites.balls.balls import *
from sprites.hills import Hills
from sprites.nicholas import Nicholas
from sprites.tartan import Tartan


class World:
    def __init__(self):
        self.sprites = Sprites([Nicholas(), Hills(), Tartan()])
        self.x = 0
        self.meters = 0
        self.running_time = 0

        self.last_background = None
        self.last_size = None

        for i in range(8):
            self.sprites.append(Cloud(3 * random.random() - 0.5))

        for i in range(10):
            self.sprites.append(Tree(3 * random.random() - 0.5))

        balls = []
        for i in range(5):
            new = random.choices([RegularBall, SmallBall, LargeBall, BouncyBall, DeadBall, BoostBall],
                                 [100, 7, 7, 5, 3, 3])
            ball = new[0](3 * random.random() - 0.5)
            if not any(b.box.intersects_with(ball.box) for b in balls):
                balls.append(ball)
                self.sprites.append(ball)

    def __update_clouds(self):
        clouds = list(self.sprites.get(Type.CLOUD))

        if len(clouds) < 10 and random.random() < 0.02:
            cloud = Cloud()
            if not any(c.box.intersects_with(cloud.box) for c in clouds):
                self.sprites.append(cloud)

    def __update_trees(self):
        trees = list(self.sprites.get(Type.TREE))

        if len(trees) < 30 and random.random() < 0.03:
            tree = Tree()
            if not any(c.box.intersects_with(tree.box) for c in trees):
                self.sprites.append(tree)

    def __update_balls(self):
        balls = list(self.sprites.get(Type.BALL))

        if len(balls) < 10 and random.random() < 0.05:
            new = random.choices([RegularBall, SmallBall, LargeBall, BouncyBall, DeadBall, BoostBall],
                                 [100, 7, 7, 5, 3, 5])
            ball = new[0]()
            if not any(b.box.intersects_with(ball.box) for b in balls):
                self.sprites.append(ball)

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
        self.__update_trees()
        self.__update_balls()

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

            font = pygame.font.Font("../res/arcade.ttf", surface.get_height() // 5)
            img = font.render(str(int(t - self.running_time) + 1), True, (0, 0, 0))
            surface.blit(img, (
                surface.get_width() // 2 - img.get_width() // 2,
                surface.get_height() // 2 - img.get_height() // 2
            ))
        else:
            font = pygame.font.Font("../res/arcade.ttf", surface.get_height() // 10)
            img = font.render(str(int(self.meters)), True, (0, 0, 0))
            surface.blit(img, (int(surface.get_width() * 0.95) - img.get_width(), int(surface.get_height() * 0.05)))
