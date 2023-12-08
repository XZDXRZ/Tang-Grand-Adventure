# Defined all bosses

import pygame, math
import game_const, player

class Lance(pygame.sprite.Sprite):
    def __init__(self):
        super(Lance, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("./assets/boss/lance/LG.PNG"), (300, 300))
        self.rect = self.image.get_rect(center = (400, 200))
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
        pass

class Lance_Big_Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, speed, time):
        super(Lance_Big_Bullet, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("./assets/boss/lance/BULLET.PNG"), (100, 100))
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = speed
        self.time = time

    def move(self):
        self.rect.left += self.speed[0]
        self.rect.top += self.speed[1]
