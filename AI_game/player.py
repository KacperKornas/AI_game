import pygame


class Player:
    def __init__(self, x, y, screen_width, screen_height):
        self.radius = 16
        self.x = int(x)
        self.y = int(y)
        self.color = (255, 102, 193)
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4
        self.screen_width = screen_width
        self.screen_height = screen_height

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def update(self):
        self.velX = 0
        self.velY = 0
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed

        self.x += self.velX
        self.y += self.velY

        self.x = max(self.radius, min(self.x, self.screen_width - self.radius))
        self.y = max(self.radius, min(self.y, self.screen_height - self.radius))
        # new_x = self.x + self.velX
        # new_y = self.y + self.velY

        # if 0 <= new_x - self.radius <= self.screen_width:
        #     self.x = new_x
        # if 800 <= new_y - self.radius <= self.screen_height:
        #     self.y = new_y

