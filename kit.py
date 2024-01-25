# 王廉威！

import pygame, numpy
import utils
from typing import Tuple

class Kit(pygame.sprite.Sprite):
    def __init__(self,
                 pos: Tuple[float, float],
                 speed: float
    ) -> None:
        super(Kit, self).__init__()

        self.image = pygame.transform.scale(
            pygame.image.load("./assets/kit/KIT.PNG"), (337/5, 512/5))
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self._speed = speed
        self._alive = True

    def _move(self) -> None:
        self.rect.centery += self._speed

        if self.rect.top > utils.SIZE["height"]:
            self._alive = False
    
    def whether_alive(self) -> bool:
        return self._alive
    
    def update(self) -> None:
        self._move()

    def display(self, screen) -> None:
        screen.blit(self.image, self.rect)

class Kit_Group(object):
    def __init__(self) -> None:
        # Creating kit group
        self._kits_group = pygame.sprite.Group()
        self._kit_drop_cd = numpy.random.normal(
            utils.KIT_CD["mean"],
            utils.KIT_CD["sd"]
        )

    def _generate_hp_kit(self) -> None:
        if self._kit_drop_cd <= 0:
            self._kits_group.add(
                Kit(
                    (numpy.random.normal(utils.SIZE["width"]/2, 200), 0),
                    utils.abs(numpy.random.normal(3, 1))
                )
            )
            self._kit_drop_cd = numpy.random.normal(
                utils.KIT_CD["mean"],
                utils.KIT_CD["sd"]
            )
        else:
            self._kit_drop_cd -= 1
        
    def get_kits_group(self) -> pygame.sprite.Group:
        return self._kits_group

    def update(self) -> None:
        self._generate_hp_kit()
        for kit in self._kits_group:
            kit.update()
            if not kit.whether_alive():
                self._kits_group.remove(kit)

    def display(self, screen) -> None:
        for kit in self._kits_group:
            kit.display(screen)
