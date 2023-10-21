import pygame


class Obstacle:
    def __init__(self, x, y, radius, screen_width, screen_height):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (0, 0, 255)
        self.screen_width = screen_width
        self.screen_height = screen_height

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
