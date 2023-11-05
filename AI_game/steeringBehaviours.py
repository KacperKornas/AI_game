from pygame.math import Vector2
import pygame
from enemy import Enemy
from matrix import Matrix
import math
import random

class SteeringBehaviours:
    
    def __init__(self, agent: Enemy) -> None:
        self.agent = agent
        
        self.theta = math.pi / 2
        self.wander_radius = 50
        self.wander_distance = 100
        self.wander_jitter = 2
        self.wander_target = Vector2(self.wander_radius * math.cos(self.theta), self.wander_radius * math.sin(self.theta))
        self.wander_point = self.agent.getHeading() * self.wander_distance + self.agent.getPos()
        self.target_pos = self.wander_point + self.wander_target
        self.max_force = 0.001
        
    def draw(self, screen):
        self.drawWander(screen)
        
    def drawWander(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.wander_point, 1, 1)
        pygame.draw.circle(screen, (255, 0, 0), self.wander_point, self.wander_radius, 1)
        pygame.draw.circle(screen, (0, 255, 100), self.target_pos, 2)
        pygame.draw.line(screen,(255, 255, 255), self.agent.getPos(), self.target_pos)
        pygame.draw.line(screen, (255, 255, 255), self.agent.getPos(), self.wander_point)
    
    def calculate(self) -> Vector2:
        steering_force = Vector2(0, 0)
        steering_force += self.wander()
        return steering_force * self.max_force
    
    def seek(self, target_pos: Vector2) -> Vector2:
        desired_vel = (target_pos - self.agent.getPos()).normalize() * self.agent.getMaxSpeed()
        return desired_vel - self.agent.getVelocity()
    
    def wander(self):
        self.wander_point = self.agent.getHeading() * self.wander_distance + self.agent.getPos()
        theta = self.theta + math.radians(Vector2(1, 0).angle_to(self.agent.getHeading()))
        self.wander_target = Vector2(self.wander_radius * math.cos(theta), self.wander_radius * math.sin(theta))
        self.target_pos = self.wander_point + self.wander_target
        displacement = 0.3
        self.theta += random.uniform(-displacement, displacement)
        return self.target_pos - self.agent.getPos()
    
    def pointToWorldSpace(self, point: Vector2, agent_heading: Vector2, agent_side: Vector2, agent_pos: Vector2):
        matrix = Matrix.rotate(agent_heading, agent_side)
        matrix = Matrix.translate(matrix, agent_pos)
        
        return Matrix.transformVector2Ds(point, matrix)      
        
        