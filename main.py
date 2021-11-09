# from space_object import SpaceObject
# def init_space_object(width, height, df, df_index):
#     df = df[df_index]
#     obj_type = str(df[0])
#     obj_info = df[1].split(",")
#     if len(obj_info) != 4:
#         raise ValueError("Error: game state incomplete")
#     else:
#         for info in obj_info:
#             try:
#                 float(info) or int(info)
#             except ValueError:
#                 raise ValueError("Error: invalid data type in line {}".format(df_index + 1))
#     x = float(obj_info[0])
#     y = float(obj_info[1])
#     angle = int(obj_info[2])%360
#     id = int(obj_info[3])

#     return SpaceObject(x, y, width, height, angle, obj_type, id)

# def read_value(df, df_index):
#     df = df[df_index]
#     try:
#         int(df[1])
#     except ValueError:
#         raise ValueError("Error: invalid data type in line {}", df_index + 1)
#     else:
#         return int(df[1])

# def import_state(game_state_filename):
#     key_set = {"width", "height", "score", "spaceship", "fuel", "asteroids_count", "asteroid_small", "asteroid_large", "bullets_count", "upcoming_asteroids_count", "upcoming_asteroid_small", "upcoming_asteroid_large"}
#     try:
#         df = open(game_state_filename, "r")
#     except FileNotFoundError:
#         raise FileNotFoundError("Error: unable to open", game_state_filename)
    
#     df = df.readlines()
#     for i in range(len(df)):
#         df[i] = df[i].split()
#         if len(df[i]) != 2:
#             raise ValueError("Error: expecting a key and value in line {}".format(i + 1))
#         if not (df[i][0] in key_set):
#             raise ValueError("Error: unexpected key: {} in line {}".format(df[i][0], i + 1))
    
#     df_index = 0
#     width = read_value(df, df_index)

#     df_index += 1 #1
#     height = read_value(df, df_index)

#     df_index += 1 #2
#     score = read_value(df, df_index)
    
#     df_index += 1 #3
#     spaceship = init_space_object(width, height, df, df_index)
    
#     df_index += 1 #4
#     fuel = read_value(df, df_index)

#     df_index += 1 #5
#     asteroids_count = read_value(df, df_index)

#     asteroids_list = []
#     for i in range(asteroids_count):
#         df_index += 1 #6 -> 6 + asteroids_count - 1
#         asteroids_list.append(init_space_object(width, height, df, df_index))

#     df_index += 1 #6 + asteroids_count
#     bullets_count = read_value(df, df_index)

#     df_index += 1 #6 + asteroids_count + 1
#     upcoming_asteroids_count = read_value(df, df_index)
    
#     upcoming_asteroids_list = []
#     for i in range(upcoming_asteroids_count):
#         df_index += 1 #6 + asteroids_count + 2 -> 6 + asteroids_count + 2 + upcomupcoming_asteroids_count - 1
#         upcoming_asteroids_list.append(init_space_object(width, height, df, df_index))

from game_engine import Engine
from gui import GUI
from player import Player

game = Engine('examples/game_state_bad.txt', Player, GUI)