# Author: Lance in Yarra
# Photoshoper: Lambert in Yarra
# Contributor: Yarra Valley ChinaTown

import pygame, numpy
import sys
import player, utils, lance

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode(
    (utils.size["width"], utils.size["height"])
)
pygame.display.set_caption("Tang Rex")

# Initialize Player
player = player.Player()

# Creating boss list and iterator for game boss
boss_list = []
boss_list.append(lance.Lance())
boss_list = iter(boss_list)

# Get the 1st boss
boss = next(boss_list)

def game_process():
    # Render Player Bullets
    for bullet in player.get_bullets_group():
        bullet.move()
        screen.blit(bullet.image, bullet.rect)
        if bullet.rect.top < 0:
            player.remove_bullet(bullet)

    # Render player
    player.move()
    screen.blit(player.image, player.rect)
    player.judge_hp_loss(boss.bullets)
    player.shoot()

    # Render Boss Bullets
    for bullet in boss.get_bullets_group():
        bullet.move()
        screen.blit(bullet.image, bullet.rect)
        if bullet.rect.top < 0 or bullet.rect.bottom > utils.size["height"] or bullet.rect.left < 0 or bullet.rect.right > utils.size["width"]:
            boss.remove_bullet(bullet)

    # Render Boss
    boss.move()
    screen.blit(boss.image, boss.rect)
    boss.judge_hp_loss(player.bullets)
    boss.shoot()

if __name__ == "__main__":
    numpy.random.seed(1919810)

    while True:
        screen.fill(utils.bg_color)

        game_process()
        
        pygame.display.flip()
        pygame.time.delay(utils.game_tick)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
