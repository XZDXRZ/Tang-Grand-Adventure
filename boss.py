# Defined all bosses

import pygame, math
import game_const, player

class Lance(pygame.sprite.Sprite):
    def __init__(self):
        super(Lance, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("./assets/boss/lance/LG.PNG"), (300, 300))
        self.rect = self.image.get_rect(center = (400, 200))
        self.mask = pygame.mask.from_surface(self.image)

        self.hp = 100
        self.bullets = pygame.sprite.Group()
        self.t = 0
        self.shoot_CD = 0

    def move(self):
        pass
    
    def loss_hp(self, bullets):
        if pygame.sprite.spritecollide(self, bullets, True, pygame.sprite.collide_mask):
            self.hp -= 1

    def func(self, x):
        return -(1.0/19)*x+14/3

    def shoot(self):
        pos = (self.rect.left, self.rect.top)
        if self.shoot_CD == 5:
            # self.bullets.add(Lance_Bullet(pos, self.t*self.func(self.t)))
            # self.bullets.add(Lance_Bullet(pos, self.t*self.func(self.t)+90))
            # self.bullets.add(Lance_Bullet(pos, self.t*self.func(self.t)+180))
            # self.bullets.add(Lance_Bullet(pos, self.t*self.func(self.t)+270))
            self.bullets.add(Lance_Bullet(pos, self.t*math.sin(self.t)))
            self.bullets.add(Lance_Bullet(pos, self.t*self.func(self.t)+90))
            self.bullets.add(Lance_Bullet(pos, self.t*self.func(self.t)+180))
            self.bullets.add(Lance_Bullet(pos, self.t*self.func(self.t)+270))
            self.shoot_CD = 0
        self.t += 0.7
        if (88 - self.t) <= 0.1:
            self.t = 0
        self.shoot_CD += 1

class Lance_Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super(Lance_Bullet, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("./assets/boss/lance/BULLET.PNG"), (50, 50))
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = math.radians(direction)

        self.speed = (math.sin(self.direction), math.cos(self.direction))

    def move(self):
        self.rect.left += self.speed[0]*3
        self.rect.top += self.speed[1]*3
