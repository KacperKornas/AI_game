import pygame
from pygame.math import Vector2

class Obstacle:
    def __init__(self, x, y, radius, screen_width, screen_height):
        # Initialize obstacle attributes
        self.pos = Vector2(x, y)
        self.radius = radius
        self.color = (0, 128, 0)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tagged = False

    def draw(self, screen):
        # Draw the obstacle as a green circle on the screen
        if not self.tagged:
            pygame.draw.circle(screen, self.color, self.pos, self.radius)
        else:
            pygame.draw.circle(screen, (128, 128, 0), self.pos, self.radius)
            
        
    def getPos(self):
        return self.pos
    
    def getRadius(self):
        return self.radius
