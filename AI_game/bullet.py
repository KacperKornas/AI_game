from pygame import Vector2
from pygame import draw

class Bullet:
    def __init__(self, world, spawn_pos: Vector2, direction: Vector2) -> None:
        self.world = world
        
        self.direction = direction
        self.velocity = direction * 2
        self.radius = 2
        self.pos = spawn_pos 
        self.color = (255, 255, 255)
        
    def getPos(self):
        return self.pos
        
    def update(self):
        self.pos += self.velocity
        
        if not self.world.isInsideScreen(self.pos):
            self.world.removeBullet(self)
        
    def draw(self, screen):
        draw.circle(screen, self.color, self.pos, self.radius)
        