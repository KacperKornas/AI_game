class World:
    def __init__(self, player, enemies, obstacles, screen_width, screen_height):
        self.player = player
        self.player.setWorld(self)
        
        self.enemies = enemies
        self.obstacles = obstacles
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bullets = []
        
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
        # if sourceAgent.is_attacking:
        #     return
        
        tagRadius = 50
        toTag = []
        
        for enemy in self.enemies:
            if enemy is sourceAgent: continue
            
            distance = (sourceAgent.getPos() - enemy.getPos()).length_squared()
            
            if distance < tagRadius * tagRadius:
                toTag.append(enemy)
            
        sourceAgent.setNeighbors(toTag)
        
        toTag.append(sourceAgent)
        
                
    def isInsideScreen(self, pos):
        return pos.x > 0 and pos.x < self.screen_width and pos.y > 0 and pos.y < self.screen_height
    
    def addBullet(self, bullet):
        self.bullets.append(bullet)
        
    def drawBullets(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)
            
    def updateBullets(self):
        for bullet in self.bullets:
            bullet.update()
            
    def getBullets(self):
        return self.bullets
    
    def removeBullet(self, bullet):
        self.bullets.remove(bullet)
        self.player.addAttackSlot()
        
    def removeAgent(self, agent):
        if agent.is_alive:
            agent.die()
            self.enemies.remove(agent)
    