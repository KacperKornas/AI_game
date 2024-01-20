# Import the necessary modules
import pygame
import random
from battleRoyalMap import BattleRoyalMap
from bot import Bot
from botProjectile import BotProjectile

class BattleRoyalGame:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 1000, 800
        self.BattleRoyalMap = BattleRoyalMap(self.WIDTH, self.HEIGHT)
        self.bots = []
        self.botsPrjectiles = []
        
    def start(self):
        pygame.init()
        screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])  # Create a game window
        pygame.display.set_caption("Battle Royal")  # Set the game window title
        clock = pygame.time.Clock()
        black = (0, 0, 0)
        self.BattleRoyalMap.createObstacles()
        
        running = True
        last_time = pygame.time.get_ticks()
        
        
        while running:
            current_time = pygame.time.get_ticks()
            dt = (current_time - last_time) / 1000.0  # Convert to seconds
            
            # if (dt < 1) : continue
            
            last_time = current_time

            screen.fill(black)  # Clear the screen with the background color
            self.BattleRoyalMap.draw(screen)
            
            pygame.display.flip()  # Refresh the screen

            clock.tick(60)  # Limit the frame rate to 60 frames per second
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
        pygame.quit()
    
    def draw(self):
        pass
    
    def update(self):
        pass
    
    def loadMap(self):
        pass
    
    def isPathObstructed(self):
        pass
    
    def getAllBotsInFOV(self):
        pass
    
    def isSecondVisibleToFirst(self):
        pass
    
    
    
    
