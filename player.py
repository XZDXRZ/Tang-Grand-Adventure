# Class defined for Tang

import pygame
import utils

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("./assets/player/T_RED.PNG"), (129, 179))
        self.rect = self.image.get_rect(center = (300, 300))
        self.mask = pygame.mask.from_surface(self.image)

        self.hp = 5
        self.speed = 5

        self.bullets = pygame.sprite.Group()
        self.shoot_CD = 0

        self.alive = True

    def move(self):
        # 纯粹不忍心删
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_w:
        #             self.rect.top -= self.speed
        #         if event.key == pygame.K_s:
        #             self.rect.top += self.speed
        #         if event.key == pygame.K_a:
        #             self.rect.left -= self.speed
        #         if event.key == pygame.K_d:
        #             self.rect.left += self.speed
        # pygame.key.set_repeat(1)

        pos = list(pygame.mouse.get_pos())
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > utils.size["width"]:
            self.rect.right = utils.size["width"]
        elif self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > utils.size["height"]:
            self.rect.bottom = utils.size["height"]

    def judge_hp_loss(self, bullets):
        if pygame.sprite.spritecollide(self, bullets, True, pygame.sprite.collide_mask):
            self.hp -= 1
        if self.hp <= 0:
            self.alive = False

    def shoot(self):
        if self.shoot_CD == utils.player_shoot_CD:
            self.bullets.add(Player_Bullet(
                pos = (self.rect.centerx, self.rect.centery)
            ))
            self.shoot_CD = 0
        self.shoot_CD += 1
    
    def get_bullets_group(self):
        return self.bullets
    
    def remove_bullet(self, target_bullet):
        self.bullets.remove(target_bullet)

class Player_Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Player_Bullet, self).__init__()
        
        self.image = pygame.transform.scale(pygame.image.load("./assets/player/BULLET.PNG"), (50, 50))
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = 5

    def move(self):
        self.rect.centery -= self.speed
