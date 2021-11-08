import config
from space_object import SpaceObject

class Engine:
    def __init__(self, game_state_filename, player_class, gui_class):
        self.import_state(game_state_filename)
        self.player = player_class()
        self.GUI = gui_class(self.width, self.height)

    def init_space_object(width, height, list):
        obj_type = list[0]
        obj_info = list[1].split(",")
        x = obj_info[0]
        y = obj_info[1]
        angle = obj_info[2]
        id = obj_info[3]

        return SpaceObject(x, y, width, height, angle, obj_type, id)

    def import_state(self, game_state_filename):
        try:
            df = open(game_state_filename, "r")
        except FileNotFoundError:
            raise FileNotFoundError("Error: unable to open", game_state_filename)
        
        df = df.readlines()
        for i in range(len(df)):
            df[i] = df[i].split()
        
        df_index = 0
        width = df[df_index][1]

        df_index += 1 #1
        height = df[df_index][1]

        df_index += 1 #2
        score = df[df_index][1]
        
        df_index += 1 #3
        spaceship = self.init_space_object(width, height, df[df_index])
        
        df_index += 1 #4
        fuel = df[df_index][1]

        df_index += 1 #5
        asteroids_count = df[df_index][1]

        asteroids_list = []
        for i in range(asteroids_count):
            df_index += 1 #6 -> 6 + asteroids_count - 1
            asteroids_list.append(self.init_space_object(width, height, df[df_index]))

        df_index += 1 #6 + asteroids_count
        bullets_count = df[df_index][1]

        df_index += 1 #6 + asteroids_count + 1
        upcoming_asteroids_count = df[df_index][1]
        
        upcoming_asteroids_list = []
        for i in range(upcoming_asteroids_count):
            df_index += 1 #6 + asteroids_count + 2 -> 6 + asteroids_count + 2 + upcomupcoming_asteroids_count - 1
            upcoming_asteroids_list.append(self.init_space_object(width, height, df[df_index]))

    def export_state(self, game_state_filename):
        
        # Enter your code here
        
        pass

    def run_game(self):
        turn_actions = [] # thay no = queue la xong
        while True:
            if (len(turn_actions)):
                if (turn_actions[0] == "l"):
                    self.space_ship.turn_left() # goi cai method quay left
                else:
                    self.space_ship.turn_right() # goi cai method quay right -> implement them no cung tien               
                turn_actions.pop(0)    
 
            # 1. Receive player input
            [thrust, left, right, bullet] = self.player.action()
            # 2. Process game logic
            if (left or right):
                if (left and right):
                    pass
                elif (left):
                    # turn left
                    turn_actions.append(["l"]*6)
                elif (right):
                    # turn right
                    turn_actions.append(["r"]*6)
            elif (thrust):
                # thrust
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
