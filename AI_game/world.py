class World:
    def __init__(self, obstacles, screen_width, screen_height):
    # Initialize player attributes
    # self.player = player
    # self.enemies = enemies
        self.obstacles = obstacles
        self.screen_width = screen_width
        self.screen_height = screen_height
        
    def getObstaclesWithinViewRange(self, agent, boxLength):
        obstaclesWithinViewRange = []

        for obstacle in self.obstacles:
            agentObstacleLength = (obstacle.getPos() - agent.getPos()).length()
            if (abs(obstacle.getRadius() - boxLength) < agentObstacleLength < (obstacle.getRadius() + boxLength)) or (agentObstacleLength <= (abs(obstacle.getRadius() - boxLength))):
                obstaclesWithinViewRange.append(obstacle)
            # else:
            #     obstacle.tagged = False
            
        
        return obstaclesWithinViewRange
    
    def getWalls(self):
        from pygame.math import Vector2
        return [
            [Vector2(0, 0), Vector2(self.screen_width, 0)],
            [Vector2(self.screen_width, 0), Vector2(self.screen_width, self.screen_height)],
            [Vector2(self.screen_width, self.screen_height), Vector2(0, self.screen_height)],
            [Vector2(0, self.screen_height), Vector2(0, 0)]
        ]
        
    