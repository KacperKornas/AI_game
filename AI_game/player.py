import pygame
from pygame.math import Vector2


class Player:
    def __init__(self, x, y, screen_width, screen_height):
        # Initialize player attributes
        self.pos = Vector2(x, y)
        self.size = 12
        self.rotation = 0
        self.color = (255, 72, 193)
        self.vel = Vector2(0, 0)
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.vertices = [self.pos + (0, -self.size), self.pos + (-self.size, self.size), self.pos + (self.size, self.size)]

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.vertices)

    def update(self):
        # Update player position and handle movement
        self.vel = Vector2(0, 0)
        
        if self.left_pressed and not self.right_pressed:
            self.vel[0] = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.vel[0] = self.speed
        if self.up_pressed and not self.down_pressed:
            self.vel[1] = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.vel[1] = self.speed

        # self.x += self.velX
        # self.y += self.velY
        self.pos += self.vel
        print(pygame.mouse.get_pos() - self.pos)

        # Ensure the player stays within the screen boundaries
        # self.x = max(self.size, min(self.x, self.screen_width - self.size))
        # self.y = max(self.size, min(self.y, self.screen_height - self.size))
        self.pos[0] = max(self.size, min(self.pos[0], self.screen_width - self.size))
        self.pos[1] = max(self.size, min(self.pos[1], self.screen_height - self.size))
        # self.vertices = [(self.x, self.y - self.size), (self.x - self.size, self.y + self.size), (self.x + self.size, self.y + self.size)]
        self.vertices = [self.pos + (0, -self.size), self.pos + (-self.size, self.size), self.pos + (self.size, self.size)]
