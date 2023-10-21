import pygame


class CollisionDetection:
    def __init__(self, player, obstacles):
        self.player = player
        self.obstacles = obstacles

    def detect_collisions(self):
        for obstacle in self.obstacles:
            distance = pygame.math.Vector2(obstacle.x - self.player.x, obstacle.y - self.player.y)
            if distance.length() < obstacle.radius + self.player.radius:
                overlap = (obstacle.radius + self.player.radius) - distance.length()
                if distance.length() != 0:
                    overlap_vector = distance.normalize() * overlap
                    self.player.x -= overlap_vector.x
                    self.player.y -= overlap_vector.y
