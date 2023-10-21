import pygame
from obstacle import Obstacle
from player import Player
from control import Control
from colision import CollisionDetection


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

control = Control(player, obstacles, WIDTH, HEIGHT)
collision_detection = CollisionDetection(player, obstacles)

running = True


while running:
    running = control.handle_events()

    screen.fill(black)

    collision_detection.detect_collisions()

    for obstacle in obstacles:
        obstacle.draw(screen)

    player.update()
    player.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
