# Author: Lance in Yarra
# Photoshoper: Lambert in Yarra
# Contributor: Year 12 in Yarra

import pygame
import sys, random
import player, utils, boss

pygame.init()
screen = pygame.display.set_mode(utils.size)
pygame.display.set_caption("Tang in Yarra")

player = player.Player()
boss_list = []
boss_list.append(boss.Lance())
boss_list = iter(boss_list)
boss = next(boss_list)

def game_process():
    # Render Bullets
    for bullet in player.bullets:
        screen.blit(bullet.image, bullet.rect)
        bullet.move()
        if bullet.rect.top < 0:
            player.bullets.remove(bullet)

    # Render player
    screen.blit(player.image, player.rect)
    player.move()
    player.loss_hp(boss.bullets)
    player.shoot()

    # Render Boss Bullets
    for bullet in boss.bullets:
        screen.blit(bullet.image, bullet.rect)
        bullet.move(boss=boss)
        if bullet.rect.top < 0 or bullet.rect.bottom > utils.size[1] or bullet.rect.left < 0 or bullet.rect.right > utils.size[0]:
            boss.bullets.remove(bullet)

    # Render Boss
    screen.blit(boss.image, boss.rect)
    boss.move()
    boss.loss_hp(player.bullets)
    boss.shoot()

if __name__ == "__main__":
    random.seed()

    while True:
        screen.fill(utils.bg_color)

        game_process()
        
        pygame.display.flip()
        pygame.time.delay(utils.tick)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
