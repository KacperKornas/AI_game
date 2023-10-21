# Import the necessary modules
import pygame
from obstacle import Obstacle
from player import Player
from control import Control
from collision import CollisionDetection


pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])  # Create a game window
pygame.display.set_caption("Zombie mod by Kacper Kornaś and Damian Kamiński")  # Set the game window title
clock = pygame.time.Clock()
black = (0, 0, 0)

# Create the player object and set its initial position
player = Player(WIDTH/2, HEIGHT/2, WIDTH, HEIGHT)

# Define the positions and sizes of obstacles in the game
obstacle_positions = [(140, 140), (650, 600), (500, 300), (700, 100), (190, 480), (700, 300), (400, 150), (300, 700)]
obstacle_radius = [100, 80, 70, 50, 60, 40, 50, 70]

# Create obstacle objects based on the previously defined positions and sizes
obstacles = [Obstacle(x, y, radius, WIDTH, HEIGHT) for (x, y), radius in zip(obstacle_positions, obstacle_radius)]

# Create a Control object that manages event handling in the game
control = Control(player, obstacles, WIDTH, HEIGHT)

# Create a CollisionDetection object responsible for detecting collisions between the player and obstacles
collision_detection = CollisionDetection(player, obstacles)

# Main game loop
running = True


while running:
    running = control.handle_events()  # Handle events, such as player movement

    screen.fill(black)  # Clear the screen with the background color

    collision_detection.detect_collisions()  # Detect collisions between the player and obstacles

    for obstacle in obstacles:
        obstacle.draw(screen)  # Draw obstacles on the screen

    player.update()  # Update the player's position
    player.draw(screen)  # Draw the player on the screen

    pygame.display.flip()  # Refresh the screen

    clock.tick(60)  # Limit the frame rate to 60 frames per second

pygame.quit()