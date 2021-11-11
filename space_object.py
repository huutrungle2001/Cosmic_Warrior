import math
import config
 
 
class SpaceObject:
    # Constructor
    def __init__(self, x, y, width, height, angle, obj_type, id):
        self.x = (float(x) + int(width)) % int(width)
        self.y = (float(y) + int(height)) % int(height)
        self.width = int(width)
        self.height = int(height)
        self.angle = (int(angle) % 360 + 360) % 360
        self.obj_type = obj_type
        self.id = int(id)
 
    def turn_left(self):
        self.angle += config.angle_increment
        self.angle %= 360
 
    def turn_right(self):
        self.angle -= config.angle_increment
        self.angle = (self.angle % 360 + 360) % 360
 
    def move_forward(self):
        self.x += config.speed[self.obj_type] * math.cos(math.radians(self.angle))
        self.x = (self.x + self.width) % self.width
        self.y -= config.speed[self.obj_type] * math.sin(math.radians(self.angle))
        self.y = (self.y + self.height) % self.height
 
    def move_forward_back(self):
        self.x -= (
            2 * config.speed[self.obj_type] * math.cos(math.radians(self.angle)) / 2.0
        )
        self.x = (self.x + self.width) % self.width
        self.y += (
            2 * config.speed[self.obj_type] * math.sin(math.radians(self.angle)) / 2.0
        )
        self.y = (self.y + self.height) % self.height
 
    def get_xy(self):
        return (self.x, self.y-(1e-14))
 
    def distance(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2
 
    def collide_with(self, other):
        return (
            self.distance(other)
            <= (config.radius[self.obj_type] + config.radius[other.obj_type]) ** 2
        )
 
    def __repr__(self):
        return "{type} {x:.1f},{y:.1f},{angle},{id}".format(
            type=self.obj_type, x=self.x, y=self.y, angle=self.angle, id=self.id
        )
 