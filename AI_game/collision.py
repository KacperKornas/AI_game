import pygame


class CollisionDetection:
    def __init__(self, player, obstacles):
        # Initialize CollisionDetection with player and obstacles
        self.player = player
        self.obstacles = obstacles

    def detect_collisions(self):
        # Detect collisions between the player and obstacles
        for obstacle in self.obstacles:
            # Calculate the distance vector between the player and the obstacle
            distance = pygame.math.Vector2(obstacle.x - self.player.x, obstacle.y - self.player.y)
            # if distance.length() < obstacle.radius + self.player.radius:
            #     # Check if the distance is less than the sum of the radii (collision detected)
            #     overlap = (obstacle.radius + self.player.radius) - distance.length()
            #     if distance.length() != 0:
            #         # Prevent division by zero if the distance is zero
            #         overlap_vector = distance.normalize() * overlap
            #         # Calculate the overlap vector to resolve the collision
            #         self.player.x -= overlap_vector.x  # Adjust the player's x-coordinate
            #         self.player.y -= overlap_vector.y  # Adjust the player's y-coordinate
