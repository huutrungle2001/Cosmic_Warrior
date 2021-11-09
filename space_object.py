import math
import config

class SpaceObject:
    # Constructor
    def __init__(self, x, y, width, height, angle, obj_type, id):
        self.x = float(x)
        self.y = float(y)
        self.width = int(width)
        self.height = int(height)
        self.angle = int(angle)%360
        self.obj_type = str(obj_type)
        self.id = int(id)

    def turn_left(self):
        self.angle += int(config.angle_increment)

    def turn_right(self):
        self.angle -= int(config.angle_increment)

    def move_forward(self):
        self.x += int(config.speed[str(self.obj_type)])*math.cos(math.radians(int(self.angle)))
        self.y += int(config.speed[str(self.obj_type)])*math.sin(math.radians(int(self.angle)))   
    
    def get_xy(self):
        return (self.x, self.y)

    def distance(self, other):
        return math.sqrt((float(self.x) - float(other.x))**2 + (float(self.y) - float(other.y))**2)

    def collide_with(self, other):
        return self.distance(other) <= (int(config.radius[str(self.obj_type)]) + int(config.radius[str(other.obj_type)]))

    def __repr__(self):
        return "{type} {x:.1f},{y:.1f},{angle},{id}".format(type = str(self.obj_type), x = float(self.get_xy()[0]), y = float(self.get_xy()[1]), angle = int(self.angle), id = int(self.id))