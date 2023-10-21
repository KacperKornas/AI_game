import pygame


class Control:
    def __init__(self, player, obstacles, WIDTH, HEIGHT):
        self.player = player
        self.obstacles = obstacles
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.left_pressed = True
                if event.key == pygame.K_RIGHT:
                    self.player.right_pressed = True
                if event.key == pygame.K_UP:
                    self.player.up_pressed = True
                if event.key == pygame.K_DOWN:
                    self.player.down_pressed = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.left_pressed = False
                if event.key == pygame.K_RIGHT:
                    self.player.right_pressed = False
                if event.key == pygame.K_UP:
                    self.player.up_pressed = False
                if event.key == pygame.K_DOWN:
                    self.player.down_pressed = False

        return True
