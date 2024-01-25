# 磊↓那↑

import pygame
import utils
from typing import Tuple

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super(Player, self).__init__()

        self.image = pygame.transform.scale(
            pygame.image.load("./assets/player/T_RED.PNG"), (129, 179))
        self.rect = self.image.get_rect(center = (300, 300))
        self.mask = pygame.mask.from_surface(self.image)

        self._hp = utils.PLAYER_MAX_HP
        self._speed = 5

        self._bullets_group = pygame.sprite.Group()
        self._shoot_CD = 0

        self._alive = True

    def _move(self) -> None:
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
        elif self.rect.right > utils.SIZE["width"]:
            self.rect.right = utils.SIZE["width"]
        elif self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > utils.SIZE["height"]:
            self.rect.bottom = utils.SIZE["height"]

    def _judge_hp_loss(self,
                      bullets: pygame.sprite.Group
    ) -> None:
        if pygame.sprite.spritecollide(self, bullets, True, pygame.sprite.collide_mask):
            # Delete the bullet after collision
            # And minus 1 hp
            self._hp -= 1
        if self._hp <= 0:
            # Killed if hp drop to 0
            self._alive = False

    def _judge_hp_gain(self,
                      kit_group: pygame.sprite.Group
    ) -> None:
        if pygame.sprite.spritecollide(self, kit_group, True, pygame.sprite.collide_mask)\
        and self._hp < utils.PLAYER_MAX_HP:
            self._hp += 1

    def _shoot(self) -> None:
        if self._shoot_CD == utils.PLAYER_SHOOT_CD:
            self._bullets_group.add(Player_Bullet(
                pos = (self.rect.centerx, self.rect.centery)
            ))
            self._shoot_CD = 0
        self._shoot_CD += 1
    
    def get_bullets_group(self) -> pygame.sprite.Group:
        return self._bullets_group
    
    def remove_bullet(self,
                      target_bullet: pygame.sprite.Sprite
    ) -> None:
        self._bullets_group.remove(target_bullet)
    
    def whether_alive(self) -> bool:
        return self._alive
    
    def update(self, boss_bullets_group, kits_group) -> None:
        self._move()
        self._shoot()

        for bullet in self._bullets_group:
            bullet.update()
            if not bullet.whether_alive():
                self._bullets_group.remove(bullet)

        # judge HP status
        self._judge_hp_loss(boss_bullets_group)
        self._judge_hp_gain(kits_group)

    def display(self, screen) -> None:
        screen.blit(self.image, self.rect)
        for bullet in self._bullets_group:
            bullet.display(screen)

class Player_Bullet(pygame.sprite.Sprite):
    def __init__(self,
                 pos: Tuple[float, float]
    ) -> None:
        super(Player_Bullet, self).__init__()

        self.image = pygame.transform.scale(
            pygame.image.load("./assets/player/BULLET.PNG"), (50, 50))
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self._speed = 5
        self._alive = True

    def _move(self) -> None:
        self.rect.centery -= self._speed

    def whether_alive(self) -> bool:
        return self._alive

    def update(self) -> None:
        self._move()

        # Life-cycle management
        if self.rect.top > utils.SIZE["height"]:
            self._alive = False

    def display(self, screen) -> None:
        screen.blit(self.image, self.rect)
