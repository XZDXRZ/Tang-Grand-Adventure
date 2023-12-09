# Defined all bosses

import pygame
import numpy
import utils

class Lance(pygame.sprite.Sprite):
    def __init__(self):
        super(Lance, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("./assets/boss/lance/LG.PNG"), (200, 200))
        self.rect = self.image.get_rect(center = (500, 100))
        self.mask = pygame.mask.from_surface(self.image)
        self.height = self.rect.bottom - self.rect.top
        self.width = self.rect.right - self.rect.left

        self.hp = 100
        self.bullets = pygame.sprite.Group()
        self.shoot_CD = 0

    def move(self):
        pass
    
    def loss_hp(self, bullets):
        if pygame.sprite.spritecollide(self, bullets, True, pygame.sprite.collide_mask):
            self.hp -= 1

    def shoot(self):
        if self.shoot_CD <= 0:
            self.bullets.add(Lance_Big_Bullet(
                pos = (self.rect.left+self.width/2, self.rect.top+self.height/2),
                horizontal_speed = utils.normal_random(-2, 0.1),
                vertical_speed = utils.normal_random(3, 0.1),
                horizontal_acceleration = utils.normal_random(0.01, 0.001),
                ex_time = utils.normal_random(100, 5),
            ))
            self.bullets.add(Lance_Big_Bullet(
                pos = (self.rect.left+self.width/2, self.rect.top+self.height/2),
                horizontal_speed = utils.normal_random(2, 0.1),
                vertical_speed = utils.normal_random(3, 0.1),
                horizontal_acceleration = utils.normal_random(-0.01, 0.001),
                ex_time = utils.normal_random(100, 5),
            ))
            self.shoot_CD = 100
        else:
            self.shoot_CD -= 1

class Lance_Big_Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, horizontal_speed, vertical_speed, horizontal_acceleration, ex_time):
        super(Lance_Big_Bullet, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("./assets/boss/lance/BULLET.PNG"), (100, 100))
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.horizontal_speed = horizontal_speed
        self.vertical_speed = vertical_speed
        self.horizontal_acceleration = horizontal_acceleration
        self.ex_time = ex_time

    def move(self, boss):
        self.rect.left += self.horizontal_speed
        self.rect.top += self.vertical_speed

        self.horizontal_speed += self.horizontal_acceleration

        self.ex_time -= 1

        if self.ex_time <= 0:
            self.explode(boss=boss)
            boss.bullets.remove(self)

    def explode(self, boss):
        for i in range(7):
            boss.bullets.add(Lance_Small_Bullet(
                pos = (self.rect.left, self.rect.top),
                speed = (utils.normal_random(0, 2), utils.normal_random(0, 2))
            ))

class Lance_Small_Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        super(Lance_Small_Bullet, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("./assets/boss/lance/BULLET.PNG"), (50, 50))
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = speed

    def move(self, boss):
        self.rect.left += self.speed[0]
        self.rect.top += self.speed[1]
