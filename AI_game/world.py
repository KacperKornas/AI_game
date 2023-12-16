class World:
    def __init__(self, player, enemies, obstacles, screen_width, screen_height):
        self.player = player
        self.enemies = enemies
        self.obstacles = obstacles
        self.screen_width = screen_width
        self.screen_height = screen_height
        
    def getPlayer(self):
        return self.player
        
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
        
    
    def tagNeighbors(self, sourceAgent):
        if sourceAgent.is_attacking:
            return
        
        sourceAgent.tagged = False
        tagRadius = 50
        
        toTag = [sourceAgent]
        
        for enemy in self.enemies:
            if enemy is sourceAgent or enemy.is_attacking: continue
            
            distance = (sourceAgent.getPos() - enemy.getPos()).length_squared()
            
            if distance < tagRadius * tagRadius:
                toTag.append(enemy)
            
        
        if len(toTag) > 10:
            for enemy in toTag:
                enemy.color = (255, 0, 0)
                enemy.tagged = True
                enemy.readyToAttack()
    
    def unTagNeighbors(self):
        pass
        
    