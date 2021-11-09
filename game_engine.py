import config
from space_object import SpaceObject


class Engine:
    def __init__(self, game_state_filename, player_class, gui_class):
        self.import_state(game_state_filename)
        self.player = player_class()
        self.GUI = gui_class(self.width, self.height)

    def init_space_object(self, width, height, df, df_index):
        df = df[df_index]
        obj_type = str(df[0])
        obj_info = df[1].split(",")
        if len(obj_info) != 4:
            raise ValueError("Error: game state incomplete")
        else:
            for info in obj_info:
                try:
                    float(info) or int(info)
                except ValueError:
                    raise ValueError(
                        "Error: invalid data type in line {line}".format(line=df_index + 1))
        x = float(obj_info[0])
        y = float(obj_info[1])
        angle = int(obj_info[2]) % 360
        id = int(obj_info[3])

        return SpaceObject(x, y, width, height, angle, obj_type, id)

    def read_value(self, df, df_index):
        df = df[df_index]
        try:
            int(df[1])
        except ValueError:
            raise ValueError(
                "Error: invalid data type in line {line}", line=df_index + 1)
        else:
            return int(df[1])

    def check_key(self, df, df_index, valid_key, key_set):
        df = df[df_index]
        if (str(df[0]) not in valid_key) or (str(df[0]) not in key_set):
            raise ValueError("Error: unexpected key: {key} in line {line}".format(
                key=str(df[0]), line=df_index + 1))

    def import_state(self, game_state_filename):
        key_set = {"width", "height", "score", "spaceship", "fuel", "asteroids_count", "asteroid_small", "asteroid_large",
                   "bullets_count", "upcoming_asteroids_count", "upcoming_asteroid_small", "upcoming_asteroid_large"}
        try:
            df = open(game_state_filename, "r")
        except FileNotFoundError:
            raise FileNotFoundError(
                "Error: unable to open", game_state_filename)

        df = df.readlines()
        for i in range(len(df)):
            df[i] = df[i].split()
            if len(df[i]) != 2:
                raise ValueError(
                    "Error: expecting a key and value in line {line}".format(line=i + 1))

        df_index = 0
        self.check_key(df, df_index, {"width"}, key_set)
        self.width = self.read_value(df, df_index)

        df_index += 1  # 1
        self.check_key(df, df_index, {"height"}, key_set)
        self.height = self.read_value(df, df_index)

        df_index += 1  # 2
        self.check_key(df, df_index, {"score"}, key_set)
        self.score = self.read_value(df, df_index)

        df_index += 1  # 3
        self.check_key(df, df_index, {"spaceship"}, key_set)
        self.spaceship = self.init_space_object(
            self.width, self.height, df, df_index)

        df_index += 1  # 4
        self.check_key(df, df_index, {"fuel"}, key_set)
        self.fuel = self.read_value(df, df_index)

        df_index += 1  # 5
        self.check_key(df, df_index, {"asteroids_count"}, key_set)
        self.asteroids_count = self.read_value(df, df_index)

        self.asteroids_list = []
        for i in range(self.asteroids_count):
            df_index += 1  # 6 -> 6 + asteroids_count - 1
            self.check_key(
                df, df_index, {"asteroid_large", "asteroid_small"}, key_set)
            self.asteroids_list.append(self.init_space_object(
                self.width, self.height, df, df_index))

        df_index += 1  # 6 + asteroids_count
        self.check_key(df, df_index, {"bullets_count"}, key_set)
        self.bullets_count = self.read_value(df, df_index)

        df_index += 1  # 6 + asteroids_count + 1
        self.check_key(df, df_index, {"upcoming_asteroids_count"}, key_set)
        self.upcoming_asteroids_count = self.read_value(df, df_index)

        self.upcoming_asteroids_list = []
        for i in range(self.upcoming_asteroids_count):
            df_index += 1  # 6 + asteroids_count + 2 -> 6 + asteroids_count + 2 + upcomupcoming_asteroids_count - 1
            self.check_key(
                df, df_index, {"upcoming_asteroid_large", "upcoming_asteroid_small"}, key_set)
            self.upcoming_asteroids_list.append(
                self.init_space_object(self.width, self.height, df, df_index))

    def to_string_space_obj(self, obj):
        return "{type} {x},{y},{angle},{id}\n".format(type=obj.obj_type, x=obj.x, y=obj.y, angle=obj.angle, id=obj.id)

    def export_state(self, game_state_filename):
        f = open(game_state_filename, 'w')
        f.write("width " + str(self.width) + "\n")
        f.write("height " + str(self.height) + "\n")
        f.write("score " + str(self.score) + "\n")
        f.write(self.to_string_space_obj(self.spaceship))
        f.write("fuel " + str(self.fuel) + "\n")
        f.write("asteroids_count " + str(self.asteroids_count) + "\n")
        for asteroid in self.asteroids_list:
            f.write(self.to_string_space_obj(asteroid))
        f.write("bullets_count " + str(self.bullets_count) + "\n")
        f.write("upcoming_asteroids_count " + str(self.upcoming_asteroids_count) + "\n")
        for upcoming_asteroid in self.upcoming_asteroids_list:
            f.write(self.to_string_space_obj(upcoming_asteroid))

    def run_game(self):
        turn_actions = []  # thay no = queue la xong
        bullets_firing = []  # danh sach cac bullets dang fire
        bullets_starting_locations = []  # danh sach cac bullets dang fire

        FUEL_VOLUME = 0  # maximum volume of fuel - no idea about this parameter

        # range of the bullet - have not found the value for this constant
        BULLET_RANGE = int(config.speed["bullet"]) * \
            int(config.bullet_move_count)

        while True:
            # 1. Manoeuvre the spaceship as per the Player's input
            if self.fuel == 0:  # no more fuel
                break
            # Print out the following warning message when fuel remaining drops
            # to or below the fuel warning thresholds (eg 75%, 50% and 25%):
            if self.fuel < int(config.fuel_warning_threshold[0]) * FUEL_VOLUME:
                print("{}% fuel warning: {} remaining".format(
                    int(config.fuel_warning_threshold[0]), self.fuel))
            elif self.fuel < int(config.fuel_warning_threshold[1]) * FUEL_VOLUME:
                print("{}% fuel warning: {} remaining".format(
                    int(config.fuel_warning_threshold[1]), self.fuel))
            elif self.fuel < int(config.fuel_warning_threshold[2]) * FUEL_VOLUME:
                print("{}% fuel warning: {} remaining".format(
                    int(config.fuel_warning_threshold[2]), self.fuel))

            self.fuel -= 1  # fuel consuming by default

            if len(turn_actions):
                if turn_actions[0] == "l":
                    self.spaceship.turn_left()  # goi cai method quay left
                else:
                    # goi cai method quay right -> implement them no cung tien
                    self.spaceship.turn_right()
                turn_actions.pop(0)

            self.spaceship.move_forward()  # move forward the space ship

            ################
            # 2. Update positions of asteroids by calling move_forward() for each asteroid
            for asteroid in self.asteroids_list:
                asteroid.move_forward()

            # 3. Update positions of bullets:
            for i in range(len(bullets_firing)):
                # Launch a new bullet if instructed by Player
                # If fuel is less than the Minimum fuel to shoot bullet constant, do not launch the bullet
                if self.fuel <= int(config.shoot_fuel_threshold):
                    print("Cannot shoot due to low fuel")
                else:
                    # New bullet has the same position as
                    new_bullet = new_bullet.copy(self.spaceship)
                    bullets_firing.append()
                bullets_firing[i].move_forward()
                # remove expired bullets (those that have travelled more than the "Bullet range" constant)
                #
                if (bullets_firing[i].distance(bullets_starting_locations[i]) > BULLET_RANGE):
                    bullets_starting_locations.remove(i)
                    bullets_firing.remove(i)

            ################
            # 1. Receive player input
            [thrust, left, right, bullet] = self.player.action(
                self.spaceship, self.asteroids_list, bullets_firing, self.fuel, self.score)
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
