# 兰斯寄！

from typing import Tuple
import pygame, numpy
import utils

big_bullet_image_list = [
    pygame.transform.scale(pygame.image.load("./assets/boss/lance/111.png"), (1629/7, 202/7)),
    pygame.transform.scale(pygame.image.load("./assets/boss/lance/112.png"), (480/1.3, 108/1.3)),
    pygame.transform.scale(pygame.image.load("./assets/boss/lance/113.png"), (480/2.3, 66/2.3))
]

small_bullet_image_list = [
    pygame.transform.scale(pygame.image.load("./assets/boss/lance/"+str(i)+".png"), (25, 25)) for i in range(1, 12)
]

class Lance(pygame.sprite.Sprite):
    def __init__(self):
        super(Lance, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("./assets/boss/lance/LANCE.PNG"), (200, 200))
        self.rect = self.image.get_rect(center = (utils.SIZE["width"]/2, 90))
        self.mask = pygame.mask.from_surface(self.image)

        self._hp = 50
        self._bullets_group = pygame.sprite.Group()
        self._shoot_CD = 0

        self._alive = True

    def _move(self):
        self.rect.centerx += numpy.random.normal(0, 10)
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
        if self._shoot_CD <= 0:
            self._bullets_group.add(Lance_Big_Bullet(
                image_number = numpy.random.randint(0, 3),
                pos = (self.rect.centerx, self.rect.centery),
                horizontal_speed = numpy.random.normal(-2, 0.1),
                vertical_speed = numpy.random.normal(3, 0.1),
                horizontal_acceleration = numpy.random.normal(0.01, 0.001),
                explode_time = numpy.random.normal(70, 5),
            ))
            self._bullets_group.add(Lance_Big_Bullet(
                image_number = numpy.random.randint(0, 3),
                pos = (self.rect.centerx, self.rect.centery),
                horizontal_speed = numpy.random.normal(2, 0.1),
                vertical_speed = numpy.random.normal(3, 0.1),
                horizontal_acceleration = numpy.random.normal(-0.01, 0.001),
                explode_time = numpy.random.normal(70, 5),
            ))
            self._shoot_CD = 100
        else:
            self._shoot_CD -= 1
                
    def get_bullets_group(self) -> pygame.sprite.Group:
        return self._bullets_group
    
    def _generate_small_bullet(self, bullet):
        for times in range(4):
            self._bullets_group.add(Lance_Small_Bullet(
                pos = (bullet.rect.centerx, bullet.rect.centery),
                speed = (
                    utils.random_sign() * (numpy.random.random()*3 + 1),
                    utils.random_sign() * (numpy.random.random()*3 + 1)
                )
            ))

    def whether_alive(self) -> bool:
        return self._alive

    def update(self, player_bullets_group):
        self._move()
        self._shoot()
        self._judge_hp_loss(player_bullets_group)
        for bullet in self._bullets_group:
            bullet.update()
            if not bullet.whether_alive():
                if bullet.is_big():
                    self._generate_small_bullet(bullet)
                self._bullets_group.remove(bullet)
    
    def display(self, screen):
        screen.blit(self.image, self.rect)
        
        for bullet in self._bullets_group:
            bullet.display(screen)

class Lance_Big_Bullet(pygame.sprite.Sprite):
    def __init__(self,
                 image_number: int,
                 pos: Tuple[float, float],
                 horizontal_speed: float,
                 vertical_speed: float,
                 horizontal_acceleration: float,
                 explode_time: float
    ):
        super(Lance_Big_Bullet, self).__init__()

        self.image = big_bullet_image_list[image_number]
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self._horizontal_speed = horizontal_speed
        self._vertical_speed = vertical_speed
        self._horizontal_acceleration = horizontal_acceleration
        self._explode_time = explode_time

        self._alive = True

    def _move(self):
        self.rect.centerx += self._horizontal_speed
        self.rect.centery += self._vertical_speed

        self._horizontal_speed += self._horizontal_acceleration

        self._explode_time -= 1

        if self._explode_time <= 0:
            self._alive = False
    
    def is_big(self):
        return True
    
    def whether_alive(self) -> bool:
        return self._alive
    
    def update(self):
        self._move()
    
    def display(self, screen):
        screen.blit(self.image, self.rect)

class Lance_Small_Bullet(pygame.sprite.Sprite):
    def __init__(self,
                 pos: Tuple[float, float],
                 speed: float
    ):
        super(Lance_Small_Bullet, self).__init__()

        self._image_id = 0

        self.image = small_bullet_image_list[self._image_id]
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self._speed = speed
        self._alive = True

    def _move(self):
        self.rect.centerx += self._speed[0]
        self.rect.centery += self._speed[1]

        if self.rect.left < 0 or \
            self.rect.right > utils.SIZE["width"] or \
            self.rect.top < 0 or \
            self.rect.bottom > utils.SIZE["height"]:
            self._alive = False

    def is_big(self):
        return False

    def _change_image(self):
        self._image_id += 1
        if self._image_id == len(small_bullet_image_list):
            self._image_id = 0
        
        self.image = small_bullet_image_list[self._image_id]

    def whether_alive(self) -> bool:
        return self._alive

    def update(self):
        self._move()
        self._change_image()
    
    def display(self, screen):
        screen.blit(self.image, self.rect)
