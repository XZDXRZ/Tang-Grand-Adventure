# 磊↓那↑

import pygame
import utils
from typing import Tuple

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("./assets/player/T_RED.PNG"), (129, 179))
        self.rect = self.image.get_rect(center = (300, 300))
        self.mask = pygame.mask.from_surface(self.image)

        self._hp = utils.player_max_hp
        self._speed = 5

        self._bullets = pygame.sprite.Group()
        self._shoot_CD = 0

        self._alive = True

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

        # Get the position of the mouse
        pos = list(pygame.mouse.get_pos())
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

        # Preventing go out of screen
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
            # Delete the bullet after collision
            # And minus 1 hp
            self._hp -= 1
        if self._hp <= 0:
            # Killed if hp drop to 0
            self._alive = False

    def judge_hp_gain(self,
                      kit_group: pygame.sprite.Group
    ):
        if pygame.sprite.spritecollide(self, kit_group, True, pygame.sprite.collide_mask) and self._hp < utils.player_max_hp:
            self._hp += 1

    def shoot(self):
        if self._shoot_CD == utils.player_shoot_CD:
            self._bullets.add(Player_Bullet(
                pos = (self.rect.centerx, self.rect.centery)
            ))
            self._shoot_CD = 0
        self._shoot_CD += 1
    
    def get_bullets_group(self) -> bool:
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

class Player_Bullet(pygame.sprite.Sprite):
    def __init__(self,
                 pos: Tuple[float, float]
    ):
        super(Player_Bullet, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("./assets/player/BULLET.PNG"), (50, 50))
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self._speed = 5

    def move(self):
        self.rect.centery -= self._speed
