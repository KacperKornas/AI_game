class World:
    def __init__(self, obstacles):
    # Initialize player attributes
    # self.player = player
    # self.enemies = enemies
        self.obstacles = obstacles
        
    def getObstaclesWithinViewRange(self, agent, boxLength):
        obstaclesWithinViewRange = []

        for obstacle in self.obstacles:
            agentObstacleLength = (obstacle.getPos() - agent.getPos()).length()
            if (abs(obstacle.getRadius() - boxLength) < agentObstacleLength < (obstacle.getRadius() + boxLength)) or (agentObstacleLength <= (abs(obstacle.getRadius() - boxLength))):
                obstaclesWithinViewRange.append(obstacle)
            # else:
            #     obstacle.tagged = False
            
        
        return obstaclesWithinViewRange
        
    