import pygame
from pygame.math import Vector2


class CollisionDetection:
    def __init__(self, player, enemies, obstacles, world):
        # Initialize CollisionDetection with player and obstacles
        self.player = player
        self.obstacles = obstacles
        self.enemies = enemies
        self.world = world

    def detect_collisions(self):
        # Detect collisions between the player and obstacles
        for obstacle in self.obstacles:
            for enemy in self.enemies:
                distance = obstacle.getPos() - enemy.getPos() 
                if distance.length() != 0 and distance.length() < obstacle.radius + enemy.radius:
                    overlap = (obstacle.radius + enemy.radius) - distance.length()
                    overlap_vector = distance.normalize() * overlap
                    enemy.pos -= overlap_vector
        #     # Calculate the distance vector between the player and the obstacle
            distance = obstacle.getPos() - self.player.pos
            if distance.length_squared() != 0 and distance.length() < obstacle.radius + self.player.size:
                # Check if the distance is less than the sum of the radii (collision detected)
                overlap = (obstacle.radius + self.player.size) - distance.length()
                # Prevent division by zero if the distance is zero
                overlap_vector = distance.normalize() * overlap
                # Calculate the overlap vector to resolve the collision
                self.player.pos -= overlap_vector
                
            for bullet in self.world.getBullets():
                distance = (bullet.getPos() - obstacle.getPos()).length_squared()
                
                if distance != 0 and distance < (obstacle.radius + bullet.radius) * (obstacle.radius + bullet.radius):
                    self.world.removeBullet(bullet)
                
                
        for enemyA in self.enemies:
            for enemyB in self.enemies:
                if enemyA is enemyB: continue
                
                distance = enemyB.getPos() - enemyA.getPos()
                if distance.length() != 0 and distance.length() < enemyA.getRadius() + enemyB.getRadius():
                    overlap = (enemyA.getRadius() + enemyB.getRadius()) - distance.length()
                    overlap_vector = distance.normalize() * overlap
                    enemyA.pos -= overlap_vector
            
            distance = (enemyA.getPos() - self.player.getPos()).length_squared()
            if distance != 0 and distance < ((enemyA.getRadius() + self.player.getSize()) * (enemyA.getRadius() + self.player.getSize())):
                if enemyA.is_attacking:
                    self.player.hit()
                # enemyA.die()
                self.world.removeAgent(enemyA)
                
            for bullet in self.world.getBullets():
                distance = (bullet.getPos() - enemyA.getPos()).length_squared()
                
                if distance != 0 and distance < (enemyA.getRadius() + bullet.radius) * (enemyA.getRadius() + bullet.radius):
                    self.world.removeBullet(bullet)
                    self.world.removeAgent(enemyA)
                    

