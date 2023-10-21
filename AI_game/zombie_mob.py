import pygame
from obstacle import Obstacle
from player import Player


pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Zombie mod by Kacper Kornaś and Damian Kamiński")
clock = pygame.time.Clock()
black = (0, 0, 0)

player = Player(WIDTH/2, HEIGHT/2, WIDTH, HEIGHT)

obstacle_positions = [(140, 140), (650, 600), (500, 300), (700, 100), (190, 480), (700, 300), (400, 150), (300, 700)]
obstacle_radius = [100, 80, 70, 50, 60, 40, 50, 70]

obstacles = [Obstacle(x, y, radius, WIDTH, HEIGHT) for (x, y), radius in zip(obstacle_positions, obstacle_radius)]

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

    for obstacle in obstacles:
        obstacle.draw(screen)

    player.update()
    player.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
