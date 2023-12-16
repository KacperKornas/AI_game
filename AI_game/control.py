import pygame


class Control:
    def __init__(self, player, obstacles, WIDTH, HEIGHT):
        # Initialize Control class with player, obstacles, and screen dimensions
        self.player = player
        self.obstacles = obstacles
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

    def handle_events(self):
        # Handle player control events and window quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.player.left_pressed = True
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.player.right_pressed = True
                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.player.up_pressed = True
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.player.down_pressed = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.player.left_pressed = False
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.player.right_pressed = False
                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.player.up_pressed = False
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.player.down_pressed = False
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.player.attack()

        return True
