import pygame
from pygame.math import Vector2

class Enemy:
    def __init__(self, x, y, radius, screen_width, screen_height):
        # Initialize player attributes
        self.pos = Vector2(x, y)
        self.vel = Vector2(1, 0)
        self.acc = Vector2(0, 0)
        self.radius = radius
        self.color = (236, 247, 20)
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.max_speed = 2
        self.max_force = 1
        self.max_turn_rate = 10
        
        import steeringBehaviours
        self.steering = steeringBehaviours.SteeringBehaviours(self)
        
    def getPos(self) -> Vector2:
        return self.pos
    
    def getMaxSpeed(self) -> float:
        return self.max_speed
    
    def getVelocity(self) -> Vector2:
        return self.vel
    
    def getHeading(self) -> Vector2:
        return self.vel.normalize()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
        pygame.draw.line(screen, (255, 255, 255), self.pos, self.getHeading() * 20 + self.pos, 2)
        self.steering.draw(screen)
        
    def update(self, dt):
        self.acc = self.steering.calculate() # mass equals 1 for simplicity
        self.vel += (self.acc)
        
        # Speeding checking - important
        if self.vel.length() > self.max_speed:
            self.vel = self.vel.normalize()
            self.vel *= self.max_speed
        
        self.pos += self.vel
        
        self.pos[0] = max(self.radius, min(self.pos[0], self.screen_width - self.radius))
        self.pos[1] = max(self.radius, min(self.pos[1], self.screen_height - self.radius))
        