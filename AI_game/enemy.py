import pygame
from pygame.math import Vector2
from steeringBehaviours import SteeringBehaviours

class Enemy:
    def __init__(self, x, y, radius, screen_width, screen_height):
        # Initialize player attributes
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.speed = 4
        self.radius = radius
        self.color = (236, 247, 20)
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.heading_vec = Vector2(0, 0)
        self.side_vec = Vector2(0, 0)
        self.max_speed = 2
        self.max_force = 20
        self.max_turn_rate = 10
        
        self.steering = SteeringBehaviours()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
        
    def update(self):
        self.vel += self.steering.calculate()
        self.vel[0] = min(self.vel[0], self.max_speed)
        self.vel[1] = min(self.vel[1], self.max_speed)
        
        self.pos += self.vel
        
        if self.vel.length() > 0.00000001:
            self.heading_vec = self.vel.normalize()
            self.side_vec = Vector2(-self.heading_vec[1], self.heading_vec[0])
        
        self.pos[0] = max(self.radius, min(self.pos[0], self.screen_width - self.radius))
        self.pos[1] = max(self.radius, min(self.pos[1], self.screen_height - self.radius))
        