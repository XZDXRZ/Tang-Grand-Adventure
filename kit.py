# 王廉威！

import pygame, numpy
import utils
from typing import Tuple

class Kit(pygame.sprite.Sprite):
    def __init__(self,
                 pos: Tuple[float, float],
                 speed: float
    ):
        super(Kit, self).__init__()

        self.image = pygame.transform.scale(pygame.image.load("./assets/kit/KIT.PNG"), (337/5, 512/5))
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self._speed = speed
        self._existance = True

    def move(self):
        self.rect.centery += self._speed

        if self.rect.top > utils.size["height"]:
            self._existance = False
    
    def whether_exist(self) -> bool:
        return self._existance

class Kit_Group(object):
    def __init__(self):
        # Creating kit group
        self._kit_group = pygame.sprite.Group()
        self._kit_drop_cd = numpy.random.normal(
            utils.kit_cd["mean"],
            utils.kit_cd["sd"]
        )

    def generate_hp_kit(self):
        if self._kit_drop_cd <= 0:
            self._kit_group.add(
                Kit(
                    (numpy.random.normal(utils.size["width"]/2, 500), 0),
                    utils.abs(numpy.random.normal(3, 1))
                )
            )
            self._kit_drop_cd = numpy.random.normal(
                utils.kit_cd["mean"],
                utils.kit_cd["sd"]
            )
        else:
            self._kit_drop_cd -= 1

    def remove_kit(self,
                   target_kit: Kit
    ):
        self._kit_group.remove(target_kit)
    
    def get_kits_group(self):
        return self._kit_group
