from pygame.math import Vector2
import pygame
from enemy import Enemy
from matrix import Matrix
from deceleration import Deceleration
import math
import random
import sys


class SteeringBehaviours:
    
    def __init__(self, agent: Enemy) -> None:
        self.agent = agent

        # wander        
        self.theta = math.pi / 2
        self.wander_radius = self.agent.getRadius() * 10
        self.wander_distance = 100.0
        self.wander_jitter = 80.0
        self.wander_target = Vector2(self.wander_radius * math.cos(self.theta), self.wander_radius * math.sin(self.theta))
        self.wander_point = self.agent.getHeading() * self.wander_distance + self.agent.getPos()
        self.target_pos = self.wander_point + self.wander_target
        self.max_force = 0.01
        
        # obstacleAvoidance
        self.minDetectionBoxLength = agent.getRadius() * 3
        self.lateralForceMult = 5.0
        self.brakingWeight = 0.2
        self.boxLength = 0
        self.avoidObstacleForce = Vector2(0, 0)
        
        # wallAvoidance
        self.wallDetectionFeelerLength = self.agent.getRadius() * 15
        self.feelers = []
        self.dist = 0
        self.point = Vector2()
        self.wallForce = Vector2(0, 0)
        
        # hide
        self.dots = []
        self.bestHidingSpot = Vector2()
        self.isHidding = False  
        
        # arrive
        self.arrivePos = Vector2(0, 0)
        
        # forces' weights
        self.hideWeight = 0.8
        self.wanderWeight = 0.8
        self.hideCounter = 0

        # evade
        self.evadeWeight = 0.8
        
        # group steering behaviors
        
    def recalculateWeights(self):
        # EXPERIMENTAL :)
        # print("prev:", self.hideWeight, self.wanderWeight)
        self.hideCounter += 1
        if self.hideCounter % 2 == 0:
            self.hideWeight = 0.8
        else:
            self.hideWeight = random.uniform(0.0, 0.2)
        self.wanderWeight = random.uniform(0.8, 1)
        # print("new:", self.hideWeight, self.wanderWeight)
        pass
    
    def calculate(self) -> Vector2:
        steering_force = Vector2(0, 0)

        steering_force += self.evade() * self.evadeWeight
        steering_force += self.hide() * self.hideWeight
        steering_force += self.wander() * self.wanderWeight
        
        if (self.agent.is_attacking):
            steering_force = self.arrive(self.agent.getWorld().getPlayer().getPos(), Deceleration.SLOW.value)
            steering_force += self.separation(self.agent.getNeighbors()) * 100

        steering_force += self.obstacleAvoidance() * 2
        steering_force += self.wallAvoidance() * 2 
            
        return steering_force * self.max_force
        
    def draw(self, screen):
        # self.drawWander(screen)
        # self.drawObstacleAvoidance(screen)
        # self.drawWallAvoidance(screen)
        # for dot in self.dots:
        #     pygame.draw.circle(screen, (255, 0, 0), dot, 5)
        
        # # pygame.draw.circle(screen, (255,255, 0), self.arrivePos, 5)
        # pygame.draw.circle(screen, (0,255, 0), self.bestHidingSpot, 5)
        # self.dots = []
        
        pass
    
    def drawWallAvoidance(self, screen):
        if len(self.feelers) > 0:
            for feeler in self.feelers:
                pygame.draw.line(screen, (255, 255, 255), self.agent.getPos(), feeler)
            pygame.draw.line(screen, (255, 255, 255), self.agent.getPos(), self.agent.getPos() + self.wallForce)
        pass
        
    
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
    
    def seek(self, target_pos: Vector2) -> Vector2:
        desired_vel = (target_pos - self.agent.getPos()).normalize() * self.agent.getMaxSpeed()
        return desired_vel - self.agent.getVelocity()
    
    def wander(self):
        ######## base VERSION #######
        # self.wander_point = self.agent.getHeading() * self.wander_distance + self.agent.getPos()
        # theta = self.theta + math.radians(Vector2(1, 0).angle_to(self.agent.getHeading()))
        # self.wander_target = Vector2(self.wander_radius * math.cos(theta), self.wander_radius * math.sin(theta))
        # self.target_pos = self.wander_point + self.wander_target
        # displacement = 0.3
        # self.theta += random.uniform(-displacement, displacement)
        # return self.target_pos - self.agent.getPos()
        
        ##### FROM THE BOOK #####
        self.wander_point = self.agent.getHeading() * self.wander_distance + self.agent.getPos()
        self.wander_target += Vector2(random.uniform(-1, 1) * self.wander_jitter, random.uniform(-1, 1) * self.wander_jitter)
        self.wander_target = self.wander_target.normalize() * self.wander_radius
        self.target_pos = self.wander_point + self.wander_target
        target_local = Vector2(self.wander_distance, 0) + self.wander_target
        target_world = Matrix.pointToWorldSpace(target_local, self.agent.getHeading(), self.agent.getPerp(), self.agent.getPos())
        
        return target_world - self.agent.getPos()
        
    
    def obstacleAvoidance(self):
        self.boxLength = self.minDetectionBoxLength + (self.agent.getVelocity().length() / self.agent.getMaxSpeed()) * self.minDetectionBoxLength
        
        obstaclesWithinRange = self.agent.getWorld().getObstaclesWithinViewRange(self.agent, self.boxLength)
        
        closestIntersectingObstacle = None
        distToClosestIP = sys.float_info.max
        localPosOfClosestObstacle = Vector2(0, 0)
        
        for obstacle in obstaclesWithinRange:
            # obstacle.tagged = True
            localPos = Matrix.pointToLocalSpace(obstacle.getPos(), self.agent.getHeading(), self.agent.getPerp(), self.agent.getPos())
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
        
        multiplier = self.lateralForceMult + (self.boxLength - localPosOfClosestObstacle.x) / self.boxLength
        
        # lateral force
        steeringForce = Vector2(0, 0)
        steeringForce.y = (closestIntersectingObstacle.getRadius() - localPosOfClosestObstacle.y) * multiplier
        
        # braking force
        steeringForce.x = (closestIntersectingObstacle.getRadius() - localPosOfClosestObstacle.x) * self.brakingWeight
        
        self.avoidObstacleForce = Matrix.VectorToWorldSpace(steeringForce, self.agent.getHeading(), self.agent.getPerp())
        return self.avoidObstacleForce
    
    def wallAvoidance(self):
        self.createFeelers()

        walls = self.agent.getWorld().getWalls()
        self.dist = 0.0
        distToClosestIP = sys.float_info.max
        closestWall = None
        steeringForce = Vector2(0, 0)
        self.point = Vector2(0, 0)
        closestPoint = Vector2(0, 0)
        
        for feeler in self.feelers:
            for wall in walls:
                if self.lineIntersection2D(self.agent.getPos(), feeler, wall[0], wall[1]) and (self.dist < distToClosestIP):
                    distToClosestIP = self.dist
                    closestWall = wall
                    closestPoint = self.point
                    
            if closestWall is None:
                continue
            
            overShoot = feeler - closestPoint
            wallNormal = (closestWall[1] - closestWall[0]).normalize()
            wallNormal = Vector2(-wallNormal.y, wallNormal.x)
            steeringForce = wallNormal * overShoot.length()
            
            self.wallForce = steeringForce
                    
        return steeringForce

    def hide(self):
        distToClosest = sys.float_info.max
        bestHidingSpot = None
        
        for obstacle in self.agent.getWorld().obstacles:
            hidingSpot = self.getHidingPos(obstacle.getPos(), obstacle.radius, self.agent.getWorld().getPlayer().pos)
            
            self.dots.append(hidingSpot)
            
            dist = (hidingSpot - self.agent.getPos()).length()
            
            if dist < distToClosest:
                distToClosest = dist
                bestHidingSpot = hidingSpot
                
        # setting the max area for searching for hideout  
        if distToClosest > 1000:
            print("here should evade")
            pass
        
        self.arrivePos = self.arrive(bestHidingSpot, Deceleration.FAST.value)
        self.bestHidingSpot = bestHidingSpot
        
        
        return self.arrivePos
    
    
    def arrive(self, targetPos: Vector2, deceleration: int) -> Vector2:
        toTarget = targetPos - self.agent.getPos()
        dist = toTarget.length()
        
        if dist > 0:
    
            decelerationTweaker = 0.3
            speed = dist / (deceleration * decelerationTweaker)
            # speed = min(speed, self.agent.getMaxSpeed())
            desiredVelocity = toTarget * speed / dist
            return desiredVelocity - self.agent.getVelocity()
        
        return Vector2(0, 0)

    def evade(self):
        player_pos = self.agent.getWorld().getPlayer().getPos()
        dist_to_player = (player_pos - self.agent.getPos()).length()

        if dist_to_player < 50:
            czas_patrzenia_w_przod = dist_to_player / self.agent.getMaxSpeed()
            przewidywana_pozycja = player_pos + Vector2(0, 0)  # Brak prędkości, używamy tylko pozycji

            return -self.arrive(przewidywana_pozycja, Deceleration.FAST.value)

        return Vector2(0, 0)
    
    def separation(self, neighbors):
        steering_force = Vector2(0, 0)

        for neighbor in neighbors:
            if neighbor is not self.agent and neighbor.isTagged():
                to_agent = self.agent.getPos() - neighbor.getPos()
                steering_force += to_agent.normalize() / to_agent.length()
                
        return steering_force

    def createFeelers(self):
        self.feelers = [
            self.agent.getPos() + self.wallDetectionFeelerLength * self.agent.getHeading(),
            self.agent.getPos() + self.wallDetectionFeelerLength / 2.0 * self.agent.getHeading().rotate(45),
            self.agent.getPos() + self.wallDetectionFeelerLength / 2.0 * self.agent.getHeading().rotate(-45)
        ]
        
        return self.feelers
    
    def lineIntersection2D(self, A: Vector2, B: Vector2, C: Vector2, D: Vector2):
        
        rTop = (A.y-C.y)*(D.x-C.x)-(A.x-C.x)*(D.y-C.y)
        rBot = (B.x-A.x)*(D.y-C.y)-(B.y-A.y)*(D.x-C.x)
        sTop = (A.y-C.y)*(B.x-A.x)-(A.x-C.x)*(B.y-A.y)
        sBot = (B.x-A.x)*(D.y-C.y)-(B.y-A.y)*(D.x-C.x)
        
        if (rBot == 0) or (sBot == 0):
            # lines are parallel
            return False
        
        r = rTop / rBot
        s = sTop / sBot
        
        if r > 0 and r < 1 and s > 0 and s < 1:
            self.dist = A.distance_to(B) * r # check it
            self.point = A + r * (B - A)
            return True
        else:
            self.dist = 0
            return False
        
        
    def getHidingPos(self, posOb: Vector2, radiusOb: float, posTarget: Vector2) -> Vector2:
        distFromBoundry = 30.0
        distAway = radiusOb + distFromBoundry
        toOb = (posOb - posTarget).normalize()
        return (toOb * distAway) + posOb
    