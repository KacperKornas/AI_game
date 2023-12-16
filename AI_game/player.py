import pygame
from pygame.math import Vector2


class Player:
    def __init__(self, x, y, screen_width, screen_height):
        # Initialize player attributes
        self.pos = Vector2(x, y)
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
        
        self.direction = (pygame.mouse.get_pos() - self.pos).normalize()
        self.vertices = [self.direction * self.size + self.pos, 
                         self.direction.rotate(-120) * self.size + self.pos, 
                         self.direction.rotate(120) * self.size + self.pos]

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.vertices)
        pygame.draw.line(screen, pygame.Color(255, 1, 1, 0), self.pos, self.vertices[0], 2)
        pygame.draw.line(screen, pygame.Color(0, 255, 0, 0), self.pos, pygame.mouse.get_pos(), 2) # player pointing vector
        
    def getPos(self):
        return self.pos

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

