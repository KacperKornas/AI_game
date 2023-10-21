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
                return False  # Exit the game if the window is closed

            if event.type == pygame.KEYDOWN:
                # Check for keydown events (key press)
                if event.key == pygame.K_LEFT:
                    self.player.left_pressed = True
                if event.key == pygame.K_RIGHT:
                    self.player.right_pressed = True
                if event.key == pygame.K_UP:
                    self.player.up_pressed = True
                if event.key == pygame.K_DOWN:
                    self.player.down_pressed = True

            if event.type == pygame.KEYUP:
                # Check for keyup events (key release)
                if event.key == pygame.K_LEFT:
                    self.player.left_pressed = False
                if event.key == pygame.K_RIGHT:
                    self.player.right_pressed = False
                if event.key == pygame.K_UP:
                    self.player.up_pressed = False
                if event.key == pygame.K_DOWN:
                    self.player.down_pressed = False

        return True  # Continue the game loop after handling events
