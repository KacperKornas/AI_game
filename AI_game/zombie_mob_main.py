# Import the necessary modules
import pygame
from obstacle import Obstacle
from player import Player
from enemy import Enemy
from control import Control
from collision import CollisionDetection
from world import World


pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])  # Create a game window
pygame.display.set_caption("Zombie mod by Kacper Kornaś and Damian Kamiński")  # Set the game window title
clock = pygame.time.Clock()
black = (0, 0, 0)

# Create the player object and set its initial position
player = Player(WIDTH/2, HEIGHT/2, WIDTH, HEIGHT)

# Define the positions and sizes of obstacles in the game
obstacle_positions = [(140, 140), (650, 600), (500, 300), 
                      (700, 100), (190, 480), (700, 300), 
                      (400, 150), (300, 700)]
obstacle_radius = [100, 80, 70, 50, 60, 40, 50, 70]

# Create obstacle objects based on the previously defined positions and sizes
obstacles = [Obstacle(x, y, radius, WIDTH, HEIGHT) for (x, y), radius in zip(obstacle_positions, obstacle_radius)]

world = World(obstacles, WIDTH, HEIGHT)

enemies = [
    # Enemy(WIDTH / 3, HEIGHT / 4, 4, WIDTH, HEIGHT),
    # Enemy(WIDTH / 3, HEIGHT / 4, 4, WIDTH, HEIGHT),
    # Enemy(WIDTH / 3, HEIGHT / 4, 4, WIDTH, HEIGHT),
    # Enemy(WIDTH / 3, HEIGHT / 4, 4, WIDTH, HEIGHT),
    # Enemy(WIDTH / 3, HEIGHT / 4, 4, WIDTH, HEIGHT),
    # Enemy(WIDTH / 3, HEIGHT / 4, 4, WIDTH, HEIGHT),
    # Enemy(WIDTH / 3, HEIGHT / 4, 4, WIDTH, HEIGHT),
    Enemy(WIDTH / 3, HEIGHT / 4, 4, WIDTH, HEIGHT, world),
    Enemy(WIDTH / 3, HEIGHT / 4, 4, WIDTH, HEIGHT, world),
    Enemy(WIDTH / 3, HEIGHT / 4, 4, WIDTH, HEIGHT, world)
]


# Create a Control object that manages event handling in the game
control = Control(player, obstacles, WIDTH, HEIGHT)

# Create a CollisionDetection object responsible for detecting collisions between the player and obstacles
collision_detection = CollisionDetection(player, enemies, obstacles)

# Main game loop
running = True
last_time = pygame.time.get_ticks()

while running:
    running = control.handle_events()  # Handle events, such as player movement
    
    current_time = pygame.time.get_ticks()
    dt = (current_time - last_time) / 1000.0  # Convert to seconds
    
    # if (dt < 1) : continue
    
    last_time = current_time

    screen.fill(black)  # Clear the screen with the background color
    

    collision_detection.detect_collisions()  # Detect collisions between the player and obstacles
    

    for obstacle in obstacles:
        obstacle.draw(screen)  # Draw obstacles on the screen
        
    for enemy in enemies:
        enemy.update(dt)
        enemy.draw(screen)

    player.update()  # Update the player's position
    player.draw(screen)  # Draw the player on the screen
    

    pygame.display.flip()  # Refresh the screen

    clock.tick(60)  # Limit the frame rate to 60 frames per second

pygame.quit()
