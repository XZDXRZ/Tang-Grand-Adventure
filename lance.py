import pygame, numpy
import utils, boss

class Lance(boss.Boss):
    def __init__(self):
        super(Lance, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("./assets/boss/lance/LG.PNG"), (200, 200))
        self.rect = self.image.get_rect(center = (utils.size["width"]/2, 90))
        self.mask = pygame.mask.from_surface(self.image)

        self.hp = 50
        self.bullets = pygame.sprite.Group()
        self.shoot_CD = 0

        self.alive = True

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
    
    def judge_hp_loss(self, bullets):
        if pygame.sprite.spritecollide(self, bullets, True, pygame.sprite.collide_mask):
            self.hp -= 1
        if self.hp <= 0:
            self.alive = False

    def shoot(self):
        if self.shoot_CD <= 0:
            self.bullets.add(Lance_Big_Bullet(
                pos = (self.rect.centerx, self.rect.centery),
                horizontal_speed = numpy.random.normal(-2, 0.1),
                vertical_speed = numpy.random.normal(3, 0.1),
                horizontal_acceleration = numpy.random.normal(0.01, 0.001),
                explode_time = numpy.random.normal(100, 5),
            ))
            self.bullets.add(Lance_Big_Bullet(
                pos = (self.rect.centerx, self.rect.centery),
                horizontal_speed = numpy.random.normal(2, 0.1),
                vertical_speed = numpy.random.normal(3, 0.1),
                horizontal_acceleration = numpy.random.normal(-0.01, 0.001),
                explode_time = numpy.random.normal(100, 5),
            ))
            self.shoot_CD = 100
        else:
            self.shoot_CD -= 1

        self.generate_small_bullets()

    def generate_small_bullets(self):
        for bullet in self.bullets:
            if bullet.existance == False:
                self.bullets.remove(bullet)
                for times in range(7):
                    self.bullets.add(Lance_Small_Bullet(
                        pos = (bullet.rect.centerx, bullet.rect.centery),
                        speed = (numpy.random.normal(0, 2), numpy.random.normal(0, 2))
                    ))
    
    def get_bullets_group(self):
        return self.bullets
    
    def remove_bullet(self, target_bullet):
        self.bullets.remove(target_bullet)

class Lance_Big_Bullet(pygame.sprite.Sprite):
    def __init__(self, pos,
                 horizontal_speed, vertical_speed, horizontal_acceleration, explode_time):
        super(Lance_Big_Bullet, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("./assets/boss/lance/BULLET.PNG"), (100, 100))
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.horizontal_speed = horizontal_speed
        self.vertical_speed = vertical_speed
        self.horizontal_acceleration = horizontal_acceleration
        self.explode_time = explode_time

        self.existance = True

    def move(self):
        self.rect.centerx += self.horizontal_speed
        self.rect.centery += self.vertical_speed

        self.horizontal_speed += self.horizontal_acceleration

        self.explode_time -= 1

        if self.explode_time <= 0:
            self.existance = False

class Lance_Small_Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        super(Lance_Small_Bullet, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("./assets/boss/lance/BULLET.PNG"), (50, 50))
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = speed

        self.existance = True

    def move(self):
        self.rect.centerx += self.speed[0]
        self.rect.centery += self.speed[1]
