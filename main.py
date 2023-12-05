# Author: Lance in Yarra
# Photoshoper: Lambert in Yarra
# Contributor: Year 12 in Yarra

import pygame
import sys
import player, game_const, boss

pygame.init()
screen = pygame.display.set_mode(game_const.size)
pygame.display.set_caption("Tang in Yarra")

player = player.Player()
lance = boss.Lance()

boss = lance

def game_process():
    # Render player
    screen.blit(player.image, player.rect)
    player.move()
    player.loss_hp(boss.bullets)
    player.shoot()

    # Render Bullets
    for bullet in player.bullets:
        screen.blit(bullet.image, bullet.rect)
        bullet.move()
        if bullet.rect.top < 0:
            player.bullets.remove(bullet)

    # Render Boss
    screen.blit(boss.image, boss.rect)
    boss.move()
    boss.loss_hp(player.bullets)
    boss.shoot()

    # Render Boss Bullets
    for bullet in boss.bullets:
        screen.blit(bullet.image, bullet.rect)
        bullet.move()
        if bullet.rect.top < 0 or bullet.rect.bottom > game_const.size[1] or bullet.rect.left < 0 or bullet.rect.right > game_const.size[0]:
            boss.bullets.remove(bullet)

if __name__ == "__main__":
    while True:
        screen.fill(game_const.bg_color)

        game_process()
        
        pygame.display.flip()
        pygame.time.delay(game_const.tick)

        print(lance.hp)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
