import config
from space_object import SpaceObject

class Engine:
    def __init__(self, game_state_filename, player_class, gui_class):
        self.import_state(game_state_filename)
        self.player = player_class()
        self.GUI = gui_class(self.width, self.height)

    def init_space_object(self, width, height, list):
        obj_type = str(list[0])
        obj_info = list[1].split(",")
        if len(obj_info) < 4:
            raise ValueError("Error: game state incomplete")
        x = float(obj_info[0])
        y = float(obj_info[1])
        angle = int(obj_info[2])%360
        id = int(obj_info[3])

        return SpaceObject(x, y, width, height, angle, obj_type, id)

    def import_state(self, game_state_filename):
        key_set = {"width", "height", "score", "spaceship", "fuel", "asteroids_count", "asteroid_small", "asteroid_large", "bullets_count", "upcoming_asteroids_count", "upcoming_asteroid_small", "upcoming_asteroid_large"}
        try:
            df = open(game_state_filename, "r")
        except FileNotFoundError:
            raise FileNotFoundError("Error: unable to open", game_state_filename)
        
        df = df.readlines()
        for i in range(len(df)):
            df[i] = df[i].split()
            if len(df[i]) < 2:
                raise ValueError("Error: expecting a key and value in line {}".format(i))
            if not (df[i][0] in key_set):
                raise ValueError("Error: unexpected key: {} in line {}".format(df[i][0], i))
        
        df_index = 0
        self.width = int(df[df_index][1])

        df_index += 1 #1
        self.height = int(df[df_index][1])

        df_index += 1 #2
        self.score = int(df[df_index][1])
        
        df_index += 1 #3
        self.spaceship = self.init_space_object(self.width, self.height, df[df_index])
        
        df_index += 1 #4
        self.fuel = int(df[df_index][1])

        df_index += 1 #5
        self.asteroids_count = int(df[df_index][1])

        self.asteroids_list = []
        for i in range(self.asteroids_count):
            df_index += 1 #6 -> 6 + asteroids_count - 1
            self.asteroids_list.append(self.init_space_object(self.width, self.height, df[df_index]))

        df_index += 1 #6 + asteroids_count
        self.bullets_count = int(df[df_index][1])

        df_index += 1 #6 + asteroids_count + 1
        self.upcoming_asteroids_count = int(df[df_index][1])
        
        self.upcoming_asteroids_list = []
        for i in range(self.upcoming_asteroids_count):
            df_index += 1 #6 + asteroids_count + 2 -> 6 + asteroids_count + 2 + upcomupcoming_asteroids_count - 1
            self.upcoming_asteroids_list.append(self.init_space_object(self.width, self.height, df[df_index]))

    def export_state(self, game_state_filename):
        
        # Enter your code here
        
        pass

    def run_game(self):
        turn_actions = []  # thay no = queue la xong
        bullets_firing = [] # danh sach cac bullets dang fire
        bullets_starting_locations = [] # danh sach cac bullets dang fire
 
        FUEL_VOLUME = 0  # maximum volume of fuel - no idea about this parameter

        BULLET_RANGE = int(config.speed["bullet"])*int(config.bullet_move_count) # range of the bullet - have not found the value for this constant
 
        while True:
 
            if self.fuel == 0:  # no more fuel
                break
            # Print out the following warning message when fuel remaining drops
            # to or below the fuel warning thresholds (eg 75%, 50% and 25%):
            if self.fuel < int(config.fuel_warning_threshold[0]) * FUEL_VOLUME:
                print("{}% fuel warning: {} remaining".format(int(config.fuel_warning_threshold[0]), self.fuel))
            elif self.fuel < int(config.fuel_warning_threshold[1]) * FUEL_VOLUME:
                print("{}% fuel warning: {} remaining".format(int(config.fuel_warning_threshold[1]), self.fuel))
            elif self.fuel < int(config.fuel_warning_threshold[2]) * FUEL_VOLUME:
                print("{}% fuel warning: {} remaining".format(int(config.fuel_warning_threshold[2]), self.fuel))
 
            self.fuel -= 1  # fuel consuming by default
 
            if len(turn_actions):
                if turn_actions[0] == "l":
                    self.spaceship.turn_left()  # goi cai method quay left
                else:
                    self.spaceship.turn_right()  # goi cai method quay right -> implement them no cung tien
                turn_actions.pop(0)
 
            self.spaceship.move_forward()  # move forward the space ship
 
 
            ################
            for asteroid in self.asteroids_list:
                asteroid.move_forward()
 
            for i in range(len(bullets_firing)):
                bullets_firing[i].move_forward()
                # remove expired bullets (those that have travelled more than the "Bullet range" constant) 
                #  
                if (bullets_firing[i].distance(bullets_starting_locations[i]) > BULLET_RANGE):
                    bullets_starting_locations.remove(i)
                    bullets_firing.remove(i)
 
 
 
            ################
            # 1. Receive player input
            [thrust, left, right, bullet] = self.player.action(self.spaceship, self.asteroids_list, bullets_firing, self.fuel, self.score)
            # 2. Process game logic
            # The spaceship consumes one unit of fuel each frame, regardless of whether thrusters are used.
            if left or right:
                if left and right:
                    pass
                elif left:
                    # turn left
                    turn_actions.append(["l"] * 6)
                elif right:
                    # turn right
                    turn_actions.append(["r"] * 6)
 
                self.fuel -= 1  # fuel consuming by turn left / right
 
            if thrust:
                # thrust
                self.spaceship.thrust_on = True
                self.fuel -= 1  # fuel consuming by using thrust engine
            else:
                self.spaceship.thrust_on = False  # thrust off
 
            if bullet:
                pass
 
            # 3. Draw the game state on screen using the GUI class
            # self.GUI.update_frame(???)
 
            # Game loop should stop when:
            # - the spaceship runs out of fuel, or
            # - no more asteroids are available
 
            break
 
        # Display final score
        # self.GUI.finish(???)
 
    # You can add additional methods if required