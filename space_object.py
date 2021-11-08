import math
import config

class SpaceObject:
    def __init__(self, x, y, width, height, angle, obj_type, id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.obj_type = obj_type
        self.id = id

    def turn_left(self):
        self.angle += self.angle_increment

    def turn_right(self):
        self.angle -= self.angle_increment

    def move_forward(self):
        self.x += self.speed*math.cos(math.radians(self.angle))
        self.y += self.speed*math.sin(math.radians(self.angle))
    
    def get_xy(self):
        return (self.x, self.y)

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def collide_with(self, other):
        return self.distance(other) <= (self.radius + other.radius)

    def __repr__(self):
        return "{type} {x:.1f},{y:.1f},{angle},{id}".format(type = self.obj_type, x = self.get_xy()[0], y = self.get_xy()[1], angle = self.angle, id = self.id)