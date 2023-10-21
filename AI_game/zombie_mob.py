import pygame
from player import Player

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Zombie mod by Kacper Kornaś and Damian Kamiński")
clock = pygame.time.Clock()
black = (0, 0, 0)

player = Player(WIDTH/2, HEIGHT/2, WIDTH, HEIGHT)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.left_pressed = True
            if event.key == pygame.K_RIGHT:
                player.right_pressed = True
            if event.key == pygame.K_UP:
                player.up_pressed = True
            if event.key == pygame.K_DOWN:
                player.down_pressed = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.left_pressed = False
            if event.key == pygame.K_RIGHT:
                player.right_pressed = False
            if event.key == pygame.K_UP:
                player.up_pressed = False
            if event.key == pygame.K_DOWN:
                player.down_pressed = False

    screen.fill(black)

    player.update()
    player.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
