# 林晟！

import pygame
import numpy
import utils
from typing import Tuple

class Ethan(pygame.sprite.Sprite):
    def __init__(self):
        super(Ethan, self).__init__()
        self.image = pygame.image.load("./assets/boss/ethan/ETHAN.PNG")
        self.rect = self.image.get_rect(center = (utils.size["width"]/2, 90))
        self.mask = pygame.mask.from_surface(self.image)

        self._hp = 50
        self._bullets = pygame.sprite.Group()
        self._shoot_CD = 0

        self._alive = True
    
    def move(self):
        self.rect.centerx += numpy.random.normal(0, 10)
        self.rect.centery += numpy.random.normal(0, 1)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > utils.size["width"]:
            self.rect.right = utils.size["width"]
        elif self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > utils.size["height"]:
            self.rect.bottom = utils.size["height"]
    
    def judge_hp_loss(self,
                      bullets: pygame.sprite.Group
    ):
        if pygame.sprite.spritecollide(self, bullets, True, pygame.sprite.collide_mask):
            self._hp -= 1
        if self._hp <= 0:
            self._alive = False
    
    def shoot(self):
        pass

class Ethan_Small_Bullet(pygame.sprite.Sprite):
    def __init__(self,
                 pos: Tuple[float, float],
                 horizontal_speed: float,
                 vertical_speed: float):
        super(Ethan_Small_Bullet, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("./assets/boss/ethan/FINGER.PNG"), (100, 100))
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        #TODO
        self._horizontal_speed = horizontal_speed
        self._vertical_speed = vertical_speed

        self._existance = True
