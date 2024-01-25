# Author: Lance De Yarra
# Photoshoper: Lambert De Yarra
# Contributor: Yarra Valley ChinaTown

import pygame, numpy
import sys
import player, utils, lance, kit, ethan

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode(
    (utils.SIZE["width"], utils.SIZE["height"])
)
pygame.display.set_caption("垒那的精神病院大冒险")

# Initialize Player
leonard = player.Player()

# Initialize Kits
kits = kit.Kit_Group()

# Initialize Boss
# Creating boss list and iterator for game boss
boss_list = []
boss_list.append(lance.Lance())
boss_list.append(ethan.Ethan())
boss_iterator = iter(boss_list)

# DEBUG
# next(boss_iterator)

if __name__ == "__main__":
    numpy.random.seed(1919810)

    # Get the 1st boss
    boss = next(boss_iterator)
    game_running = True

    while game_running:
        screen.fill(utils.BG_COLOR)

        # Render player
        leonard.update(
            boss_bullets_group=boss.get_bullets_group(),
            kits_group=kits.get_kits_group()
        )
        leonard.display(screen)

        # Render HP Kit
        kits.update()
        kits.display(screen)

        # Render Boss
        boss.update(
            player_bullets_group=leonard.get_bullets_group()
        )
        boss.display(screen)

        # If the boss is defeated
        if boss.whether_alive() == False:
            boss = next(boss_iterator)
        
        # If the player is defeated
        if leonard.whether_alive() == False:
            game_running = False
        
        pygame.display.flip()
        pygame.time.delay(utils.GAME_TICK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
