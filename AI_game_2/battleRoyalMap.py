import pygame
from pygame import Vector2
from obstacle import Obstacle

class BattleRoyalMap:
    pass


    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.obstacles = []
        self.pointSpace = 20
        
    def createObstacles(self):

        self.obstacles.append([self.getMapPoint(0, 13), self.getMapPoint(12, 13), self.getMapPoint(12, 18), self.getMapPoint(0, 18)])
        self.obstacles.append([self.getMapPoint(16, 13), self.getMapPoint(21, 13), self.getMapPoint(21, 10), self.getMapPoint(22, 10)
                               , self.getMapPoint(22, 19),  self.getMapPoint(27, 19), self.getMapPoint(27, 20), self.getMapPoint(19, 20)
                               , self.getMapPoint(19, 33), self.getMapPoint(10, 33), self.getMapPoint(10, 30), self.getMapPoint(12, 30)
                               , self.getMapPoint(16, 21)])
        self.obstacles.append([self.getMapPoint(27, 7), self.getMapPoint(32, 7), self.getMapPoint(29.5, 11)])
        self.obstacles.append([self.getMapPoint(29.5, 11), self.getMapPoint(27, 15), self.getMapPoint(32, 15)])
        
        self.obstacles.append([self.getMapPoint(21, 6), self.getMapPoint(22, 6), self.getMapPoint(22, 0), self.getMapPoint(21, 0)])
        self.obstacles.append([self.getMapPoint(36, 6), self.getMapPoint(37, 6), self.getMapPoint(37, 0), self.getMapPoint(36, 0)])
        
        self.obstacles.append([self.getMapPoint(22, 33), self.getMapPoint(29, 33), self.getMapPoint(29, 35), self.getMapPoint(22, 35)])
        
        self.obstacles.append([self.getMapPoint(35, 33), self.getMapPoint(43, 33), self.getMapPoint(43, 28), self.getMapPoint(45, 28)
                               , self.getMapPoint(45, 35), self.getMapPoint(35, 35)])
        
        self.obstacles.append([self.getMapPoint(33, 19), self.getMapPoint(37, 19), self.getMapPoint(37, 12), self.getMapPoint(38, 12)
                               , self.getMapPoint(38, 16), self.getMapPoint(43, 16), self.getMapPoint(43, 13), self.getMapPoint(45, 13)
                               , self.getMapPoint(45, 24), self.getMapPoint(43, 24), self.getMapPoint(43, 20), self.getMapPoint(33, 20)])


        
        # pass
    
    def getBotPoint(self, x, y):
        if self.pointSpace * x > self.width or self.pointSpace * y > self.height:
            print("Point Of Range")
        return Vector2(self.pointSpace * 2 * x, self.pointSpace * y * 2)
    
    def getMapPoint(self, x, y):
        if self.pointSpace * x > self.width or self.pointSpace * y > self.height:
            print("Point Of Range")
        return Vector2(self.pointSpace * x, self.pointSpace * y)
            
    
    def draw(self, surface):
        for i in range(0, self.width, self.pointSpace * 2):
            pygame.draw.line(surface, (255, 255, 255), Vector2(i, 0), Vector2(i, self.height))
            
        for i in range(0, self.height, self.pointSpace * 2):
            pygame.draw.line(surface, (255, 255, 255), Vector2(0, i), Vector2(self.width, i))
            
        for i in range(self.pointSpace, self.width, self.pointSpace * 2):
            pygame.draw.line(surface, (105,105,105), Vector2(i, 0), Vector2(i, self.height))
            
        for i in range(self.pointSpace, self.height, self.pointSpace * 2):
            pygame.draw.line(surface, (105,105,105), Vector2(0, i), Vector2(self.width, i))
            
        pygame.draw.circle(surface, (255, 255, 255), self.getBotPoint(1, 1), 10)
        
        for obstacle in self.obstacles:
            pygame.draw.polygon(surface, (255, 255, 130), obstacle)
            