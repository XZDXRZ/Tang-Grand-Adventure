# 兰斯寄！

from typing import Tuple
import pygame, numpy
import utils

class Lance(pygame.sprite.Sprite):
    def __init__(self):
        super(Lance, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("./assets/boss/lance/LANCE.PNG"), (200, 200))
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
        if self._shoot_CD <= 0:
            self._bullets.add(Lance_Big_Bullet(
                pos = (self.rect.centerx, self.rect.centery),
                horizontal_speed = numpy.random.normal(-2, 0.1),
                vertical_speed = numpy.random.normal(3, 0.1),
                horizontal_acceleration = numpy.random.normal(0.01, 0.001),
                explode_time = numpy.random.normal(100, 5),
            ))
            self._bullets.add(Lance_Big_Bullet(
                pos = (self.rect.centerx, self.rect.centery),
                horizontal_speed = numpy.random.normal(2, 0.1),
                vertical_speed = numpy.random.normal(3, 0.1),
                horizontal_acceleration = numpy.random.normal(-0.01, 0.001),
                explode_time = numpy.random.normal(100, 5),
            ))
            self._shoot_CD = 100
        else:
            self._shoot_CD -= 1

        self.generate_small_bullets()

    def generate_small_bullets(self):
        for bullet in self._bullets:
            if bullet.whether_exist() == False:
                self._bullets.remove(bullet)
                for times in range(3):
                    # self._bullets.add(Lance_Small_Bullet(
                    #     pos = (bullet.rect.centerx, bullet.rect.centery),
                    #     speed = (numpy.random.normal(0, 2), numpy.random.normal(0, 2))
                    # ))
                    self._bullets.add(Lance_Small_Bullet(
                        pos = (bullet.rect.centerx, bullet.rect.centery),
                        speed = (
                            utils.random_sign() * (numpy.random.random()*3 + 1),
                            utils.random_sign() * (numpy.random.random()*3 + 1)
                        )
                    ))
    
    def get_bullets_group(self) -> pygame.sprite.Group:
        return self._bullets
    
    def remove_bullet(self,
                      target_bullet: pygame.sprite.Sprite
    ):
        """Remove a bullet from the bullet group in this entity.

        Args:
        - target_bullet: bullet that need to be removed.
        """
        self._bullets.remove(target_bullet)

    def whether_alive(self) -> bool:
        return self._alive

class Lance_Big_Bullet(pygame.sprite.Sprite):
    def __init__(self,
                 pos: Tuple[float, float],
                 horizontal_speed: float,
                 vertical_speed: float,
                 horizontal_acceleration: float,
                 explode_time: float
    ):
        super(Lance_Big_Bullet, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("./assets/boss/lance/INT.PNG"), (100, 100))
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self._horizontal_speed = horizontal_speed
        self._vertical_speed = vertical_speed
        self._horizontal_acceleration = horizontal_acceleration
        self._explode_time = explode_time

        self._existance = True

    def move(self):
        self.rect.centerx += self._horizontal_speed
        self.rect.centery += self._vertical_speed

        self._horizontal_speed += self._horizontal_acceleration

        self._explode_time -= 1

        if self._explode_time <= 0:
            self._existance = False
    
    def whether_exist(self) -> bool:
        return self._existance

class Lance_Small_Bullet(pygame.sprite.Sprite):
    def __init__(self,
                 pos: Tuple[float, float],
                 speed: float
    ):
        super(Lance_Small_Bullet, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("./assets/boss/lance/INT.PNG"), (50, 50))
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self._speed = speed

        self._existance = True

    def move(self):
        self.rect.centerx += self._speed[0]
        self.rect.centery += self._speed[1]

    def whether_exist(self) -> bool:
        return self._existance
