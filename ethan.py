# 林晟！

import pygame
import numpy
import utils

class Ethan(pygame.sprite.Sprite):
    def __init__(self):
        super(Ethan, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load("./assets/boss/ethan/ETHAN.PNG"), (425/2, 405/2))
        self.rect = self.image.get_rect(center = (utils.SIZE["width"]/2, 90))
        self.mask = pygame.mask.from_surface(self.image)

        self._hp = 50
        self._bullets_group = pygame.sprite.Group()
        self._shoot_CD = 0

        self._alive = True
    
    def _move(self):
        self.rect.centerx += numpy.random.normal(0, 3)
        self.rect.centery += numpy.random.normal(0, 1)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > utils.SIZE["width"]:
            self.rect.right = utils.SIZE["width"]
        elif self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > utils.SIZE["height"]:
            self.rect.bottom = utils.SIZE["height"]
    
    def _judge_hp_loss(self,
                      bullets: pygame.sprite.Group
    ):
        if pygame.sprite.spritecollide(self, bullets, True, pygame.sprite.collide_mask):
            self._hp -= 1
        if self._hp <= 0:
            self._alive = False
    
    def _shoot(self):
        if self._shoot_CD > 0:
            self._shoot_CD -= 1
            return
        self._bullets_group.add(
            Ethan_Big_Bullet(
                vertical_speed=utils.abs(numpy.random.normal(3, 3)),
            )
        )
        self._shoot_CD = 500

    def get_bullets_group(self) -> pygame.sprite.Group:
        return self._bullets_group

    def whether_alive(self) -> bool:
        return self._alive
    
    def update(self, player_bullets_group):
        self._shoot()
        self._move()
        for bullet in self._bullets_group:
            bullet.update()
            if not bullet.whether_alive():
                self._bullets_group.remove(bullet)
        self._judge_hp_loss(player_bullets_group)
    
    def display(self, screen):
        screen.blit(self.image, self.rect)
        for bullet in self._bullets_group:
            bullet.display(screen)

class Ethan_Big_Bullet(pygame.sprite.Sprite):
    def __init__(self,
                 vertical_speed: float):
        super(Ethan_Big_Bullet, self).__init__()

        self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load("./assets/boss/ethan/FINGER.PNG"), (425/2, 405/2)), angle=180)
        self.image.set_alpha(255)
        self.rect = self.image.get_rect(center = (utils.SIZE["width"]/2, 110))
        self.mask = pygame.mask.from_surface(self.image)

        self._vertical_speed = vertical_speed
        self._alpha = 0

        self._alive = True
        self._ready_to_go = False

    def _move(self):
        if self._ready_to_go:
            self.rect.centery += self._vertical_speed
    
    def _appear(self):
        if self._alpha >= 255:
            self._ready_to_go = True
            return
        self._alpha += 1
        self.image.set_alpha(self._alpha)
    
    def whether_alive(self) -> bool:
        return self._alive

    def update(self):
        self._appear()
        self._move()

        if self.rect.top > utils.SIZE["height"]:
            self._alive = False
    
    def display(self, screen):
        screen.blit(self.image, self.rect)
