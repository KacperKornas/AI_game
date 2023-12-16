import pygame
from pygame.math import Vector2

class Enemy:
    def __init__(self, x, y, radius, screen_width, screen_height, world):
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
        
        self.world = world
        
        import steeringBehaviours
        self.steering = steeringBehaviours.SteeringBehaviours(self)
        
        self.delta = 0
        self.last_time = pygame.time.get_ticks()
        self.is_attacking = False
        
        self.is_alive = True
        
        self.neighbors = []
        
    
    def getWorld(self):
        return self.world
        
    def getPos(self) -> Vector2:
        return self.pos
    
    def getMaxSpeed(self) -> float:
        return self.max_speed
    
    def getVelocity(self) -> Vector2:
        return self.vel
    
    def getHeading(self) -> Vector2:
        return self.vel.normalize()
    
    def getRadius(self) -> int:
        return self.radius
    
    def getPerp(self) -> Vector2:
        heading = self.getHeading()
        return Vector2(-heading[1], heading[0])
    
    def setNeighbors(self, neighbors):
        self.neighbors = neighbors
    
    def getNeighbors(self):
        return self.neighbors
    
    def isTagged(self):
        return self.is_attacking

    def draw(self, screen):
        if not self.is_alive: return
        
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
        self.steering.draw(screen)
        
    def readyToAttack(self):
        self.color = (255, 0, 0)
        self.is_attacking = True
        
    def prepareToAttack(self):
        if (not self.is_attacking) and len(self.neighbors) >= 10 and self.neighborsAreIdle():
            self.readyToAttack()
            
            for enemy in self.neighbors:
                if enemy.is_attacking: continue
                
                enemy.readyToAttack()
                
    def neighborsAreIdle(self):
        for neighbor in self.neighbors:
            if neighbor.is_attacking:
                return False
        
        return True
        
    def die(self):
        self.is_alive = False
        
    def update(self, dt):
        self.world.tagNeighbors(self)
        self.prepareToAttack()
        self.acc = self.steering.calculate() # mass equals 1 for simplicity
        self.vel += (self.acc)
        
        # Speeding checking - important
        if self.vel.length() > self.max_speed:
            self.vel = self.vel.normalize()
            self.vel *= self.max_speed
        
        self.pos += self.vel
        
        self.pos[0] = max(self.radius, min(self.pos[0], self.screen_width - self.radius))
        self.pos[1] = max(self.radius, min(self.pos[1], self.screen_height - self.radius))
        
        
        current_time = pygame.time.get_ticks()
        self.delta = (current_time - self.last_time) / 1000.0
        
        
        if (self.delta > 5): 
            self.steering.recalculateWeights()
            self.last_time = current_time
        