from pygame.math import Vector2
import pygame
from enemy import Enemy
from matrix import Matrix
import math
import random
import sys

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
        
        # obstacleAvoidance
        self.boxLength = 0
        self.avoidObstacleForce = Vector2(0, 0)
        
    def draw(self, screen):
        # self.drawWander(screen)
        self.drawObstacleAvoidance(screen)
        
    
    def drawObstacleAvoidance(self, screen):
        boxWidth = self.agent.getPerp() * self.agent.getRadius()
        boxEnd = self.agent.getHeading() * self.boxLength
        pygame.draw.polygon(screen, (255, 0, 0), [self.agent.getPos() - boxWidth, self.agent.getPos() + boxWidth, self.agent.getPos() + boxWidth + boxEnd , self.agent.getPos() - boxWidth + boxEnd], 1)
        pygame.draw.circle(screen, (0, 255, 100), self.agent.getPos(), self.boxLength, 1)
        if self.avoidObstacleForce.length() != 0:
            pygame.draw.line(screen,(255, 255, 255), self.agent.getPos(), self.agent.getPos() + self.avoidObstacleForce.normalize() * 10)
    
    def drawWander(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.wander_point, 1, 1)
        pygame.draw.circle(screen, (255, 0, 0), self.wander_point, self.wander_radius, 1)
        pygame.draw.circle(screen, (0, 255, 100), self.target_pos, 2)
        pygame.draw.line(screen,(255, 255, 255), self.agent.getPos(), self.target_pos)
        pygame.draw.line(screen, (255, 255, 255), self.agent.getPos(), self.wander_point)
    
    def calculate(self) -> Vector2:
        steering_force = Vector2(0, 0)
        steering_force += self.wander()
        steering_force += self.obstacleAvoidance()
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
    
    def pointToLocalSpace(self, point: Vector2, agentHeading: Vector2, agentSide: Vector2, agentPosition: Vector2):
        Tx = -agentPosition.dot(agentHeading)
        Ty = -agentPosition.dot(agentSide)
        
        matrix = [[agentHeading.x, agentSide.x, 0],
                  [agentHeading.y, agentSide.y, 0],
                  [Tx, Ty, 0]]
        
        return Matrix.transformVector2Ds(point, matrix)
    
    def VectorToWorldSpace(self, vec: Vector2, agentHeading: Vector2, agentSide: Vector2) -> Vector2:
        matrix = Matrix.rotate(agentHeading, agentSide)
        return Matrix.transformVector2Ds(vec, matrix)
    
    def obstacleAvoidance(self):
        minDetectionBoxLength = 30
        self.boxLength = minDetectionBoxLength + (self.agent.getVelocity().length() / self.agent.getMaxSpeed()) * minDetectionBoxLength
        
        obstaclesWithinRange = self.agent.getWorld().getObstaclesWithinViewRange(self.agent, self.boxLength)
        
        closestIntersectingObstacle = None
        distToClosestIP = sys.float_info.max
        localPosOfClosestObstacle = Vector2(0, 0)
        
        for obstacle in obstaclesWithinRange:
            # obstacle.tagged = True
            localPos = self.pointToLocalSpace(obstacle.getPos(), self.agent.getHeading(), self.agent.getPerp(), self.agent.getPos())
            if localPos.x < 0:
                obstacle.tagged = False
                continue
            
            expendedRadius = obstacle.getRadius() + self.agent.getRadius()
            
            if abs(localPos.y) >= expendedRadius:
                obstacle.tagged = False
                continue
            
            # //given by the formula x = cX +/-sqrt(r^2-cY^2) for y=0.
            
            sqrtPart = math.sqrt(expendedRadius * expendedRadius - localPos.y * localPos.y)
            ip = localPos.x - sqrtPart
            
            if ip <= 0:
                ip = localPos.x + sqrtPart
                
            if ip < distToClosestIP:
                distToClosestIP = ip
                closestIntersectingObstacle = obstacle
                localPosOfClosestObstacle = localPos
            
            
        if closestIntersectingObstacle is None:
            self.avoidObstacleForce = Vector2(0, 0)
            return Vector2(0, 0)
        
        multiplier = 1.0 + (self.boxLength - localPosOfClosestObstacle.x) / self.boxLength
        
        # lateral force
        steeringForce = Vector2(0, 0)
        steeringForce.y = (closestIntersectingObstacle.getRadius() - localPosOfClosestObstacle.y) * multiplier
        
        # braking force
        brakingWeight = 0.2
        steeringForce.x = (closestIntersectingObstacle.getRadius() - localPosOfClosestObstacle.x) * brakingWeight
        
        self.avoidObstacleForce = self.VectorToWorldSpace(steeringForce, self.agent.getHeading(), self.agent.getPerp())
        return self.avoidObstacleForce
        
        
        