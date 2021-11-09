import config
from space_object import SpaceObject


class Engine:
    def __init__(self, game_state_filename, player_class, gui_class):
        self.import_state(game_state_filename)
        self.player = player_class()
        self.GUI = gui_class(self.width, self.height)

    def init_space_object(self, width, height, df, df_index):
        df = df[df_index]
        obj_type = df[0]
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
        x = obj_info[0]
        y = obj_info[1]
        angle = obj_info[2]
        id = obj_info[3]

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

    def export_state(self, game_state_filename):
        f = open(game_state_filename, 'w')
        f.write("width " + str(self.width) + "\n")
        f.write("height " + str(self.height) + "\n")
        f.write("score " + str(self.score) + "\n")
        f.write(self.spaceship.__repr__())
        f.write("fuel " + str(self.fuel) + "\n")
        f.write("asteroids_count " + str(self.asteroids_count) + "\n")
        for asteroid in self.asteroids_list:
            f.write(asteroid.__repr__())
        f.write("bullets_count " + str(self.bullets_count) + "\n")
        f.write("upcoming_asteroids_count " +
                str(self.upcoming_asteroids_count) + "\n")
        for upcoming_asteroid in self.upcoming_asteroids_list:
            f.write(upcoming_asteroid.__repr__())

    def display_remaining_fuel_message(self):
        # Print out the following warning message when fuel remaining drops
        # to or below the fuel warning thresholds (eg 75%, 50% and 25%):
        if self.fuel < int(config.fuel_warning_threshold[2]) / 100.0 * self.FUEL_VOLUME:
            print(
                "{}% fuel warning: {} remaining".format(
                    int(config.fuel_warning_threshold[0]), self.fuel
                )
            )
        elif self.fuel < int(config.fuel_warning_threshold[1]) / 100.0 * self.FUEL_VOLUME:
            print(
                "{}% fuel warning: {} remaining".format(
                    int(config.fuel_warning_threshold[1]), self.fuel
                )
            )
        elif self.fuel < int(config.fuel_warning_threshold[0]) / 100.0 * self.FUEL_VOLUME:
            print(
                "{}% fuel warning: {} remaining".format(
                    int(config.fuel_warning_threshold[2]), self.fuel
                )
            )

    def run_game(self):
        turn_actions = []  # thay no = queue la xong
        bullets_firing = []  # danh sach cac bullets dang fire
        bullets_starting_locations = []  # danh sach cac bullets dang fire

        self.FUEL_VOLUME = self.fuel  # maximum volume of fuel - no idea about this parameter

        BULLET_RANGE = config.speed["bullet"] * \
            config.bullet_move_count

        while True:
            self.display_remaining_fuel_message()

            # 1. Manoeuvre the spaceship as per the Player's input
            if self.fuel == 0:  # no more fuel
                break

            self.fuel -= config.spaceship_fuel_consumption  # fuel consuming by default

            self.spaceship.move_forward()  # move forward the space ship

            ################
            # 2. Update positions of asteroids by calling move_forward() for each asteroid
            asteriods_destroyed_count = 0
            asteriods_destroyed = []
            for asteroid in self.asteroids_list:
                asteroid.move_forward()
                if (self.spaceship.collide_with(asteroid)):
                    print("Score: {score} \t [Spaceship collided with asteroid {id}]".format(
                        score=self.score, id=asteroid.id))
                    asteriods_destroyed_count += 1
                    asteriods_destroyed.append(asteroid)

            if (asteriods_destroyed_count):
                for asteriod_destroyed in asteriods_destroyed:
                    self.asteroids_list.remove(asteriod_destroyed)

                self.asteroids_count -= asteriods_destroyed_count

                if (self.upcoming_asteroids_count == 0):
                    print("Error: no more asteroids available")
                    break
                else:
                    self.asteroids_list.append(self.upcoming_asteroids_list[0])
                    self.asteroids_count += 1

                    print("Added asteroid {id}".format(
                        id=self.upcoming_asteroids_list[0].id))

                    self.upcoming_asteroids_count -= 1
                    self.upcoming_asteroids_list.pop(0)

            # 1. Receive player input
            [thrust, left, right, bullet] = self.player.action(
                self.spaceship,
                self.asteroids_list,
                bullets_firing,
                self.fuel,
                self.score
            )
            # 2. Process game logic
            # The spaceship consumes one unit of fuel each frame, regardless of whether thrusters are used.
            if left or right:
                pass

            if thrust:
                # thrust
                pass
            else:
                pass

            if bullet:
                pass

            # 3. Draw the game state on screen using the GUI class
            # self.GUI.update_frame(???)
            self.GUI.update_frame(
                self.spaceship, self.asteroids_list, self.bullet_list, self.score, self.fuel)
            # Game loop should stop when:
            # - the spaceship runs out of fuel, or
            # - no more asteroids are available

            # break

        # Display final score
        self.GUI.finish()

    # You can add additional methods if required
