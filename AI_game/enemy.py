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
        
        self.heading_vec = self.vel.normalize()
        self.side_vec = Vector2(-self.heading_vec[1], self.heading_vec[0])
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
    
    def getSide(self) -> Vector2:
        return self.side_vec

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
        pygame.draw.line(screen, (255, 255, 255), self.pos, self.getHeading() * 10 + self.pos)
        pygame.draw.line(screen, (255, 255, 255), self.pos, self.side_vec * 10 + self.pos)
        self.steering.draw(screen)
        
    def update(self, dt):
        self.acc = self.steering.calculate() # mass equals 1 for simplicity
        # print(self.vel)
        self.vel += (self.acc)
        # print(self.vel)
        # if self.vel.length_squared() > (self.max_speed * self.max_speed):
        self.vel[0] = min(self.vel[0], self.max_speed)
        self.vel[1] = min(self.vel[1], self.max_speed)
        # print(self.vel)
        
        self.pos += self.vel
        # self.acc = Vector2(0, 0)
        
        
        # if self.vel.length() > 0.00000001:
        self.heading_vec = self.vel.normalize()
        self.side_vec = Vector2(-self.heading_vec[1], self.heading_vec[0])
        
        self.pos[0] = max(self.radius, min(self.pos[0], self.screen_width - self.radius))
        self.pos[1] = max(self.radius, min(self.pos[1], self.screen_height - self.radius))
        