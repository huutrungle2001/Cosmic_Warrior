import config
from space_object import SpaceObject

class Engine:
    def __init__(self, game_state_filename, player_class, gui_class):
        self.import_state(game_state_filename)
        self.player = player_class()
        self.GUI = gui_class(self.width, self.height)

    def import_state(self, game_state_filename):
        try:
            df = open(game_state_filename, "r")
        except FileNotFoundError:
            raise FileNotFoundError("Error: unable to open", game_state_filename)
        
        df = df.readlines()
        
        

        self.width = df[0].split()[1]
        self.height = df[1].split()[1]
        self.score = df[2].split()[1]
        


    def export_state(self, game_state_filename):
        
        # Enter your code here
        
        pass

    def run_game(self):

        while True:
            # 1. Receive player input
            
            # 2. Process game logic

            # 3. Draw the game state on screen using the GUI class
            # self.GUI.update_frame(???)

            # Game loop should stop when:
            # - the spaceship runs out of fuel, or
            # - no more asteroids are available

            break

        # Display final score
        # self.GUI.finish(???)

    # You can add additional methods if required
