import pygame
from pygame.math import Vector2
from bullet import Bullet


class Player:
    def __init__(self, x, y, screen_width, screen_height):
        # Initialize player attributes
        self.pos = Vector2(x, y)
        self.health = 20
        self.size = 16
        self.color = (255, 72, 193)
        self.vel = Vector2(0, 0)
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 1.5
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world = None
        self.attacks_available = 3
        
        self.direction = (pygame.mouse.get_pos() - self.pos).normalize()
        self.vertices = [self.direction * self.size + self.pos, 
                         self.direction.rotate(-120) * self.size + self.pos, 
                         self.direction.rotate(120) * self.size + self.pos]

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.vertices)
        pygame.draw.line(screen, pygame.Color(0, 255, 0, 0), self.pos, pygame.mouse.get_pos(), 2) # player pointing vector
        self.world.drawBullets(screen)
        
    def getPos(self):
        return self.pos
    
    def getSize(self):
        return self.size

    def update(self):
        self.vel = Vector2(0, 0)
        
        if self.left_pressed and not self.right_pressed:
            self.vel[0] = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.vel[0] = self.speed
        if self.up_pressed and not self.down_pressed:
            self.vel[1] = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.vel[1] = self.speed

        self.pos += self.vel

        self.pos[0] = max(self.size, min(self.pos[0], self.screen_width - self.size))
        self.pos[1] = max(self.size, min(self.pos[1], self.screen_height - self.size))
        
        direction = (pygame.mouse.get_pos() - self.pos).normalize()
        self.vertices = [direction * self.size + self.pos, 
                         direction.rotate(-120) * self.size + self.pos, 
                         direction.rotate(120) * self.size + self.pos]
        
        self.world.updateBullets()
        
    def setWorld(self, world):
        self.world = world
        
    def hit(self):
        self.health -= 2
        print("health remaining: ", self.health)
        pass
    
    def attack(self):
        if self.attacks_available < 1: return
        
        direction = (pygame.mouse.get_pos() - self.pos).normalize()
        bullet = Bullet(self.world, self.pos + direction * self.size, direction)
        self.world.addBullet(bullet)
        self.attacks_available -= 1
        
    def addAttackSlot(self):
        self.attacks_available += 1
                    

