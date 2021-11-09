key_set = {"width", "height", "score", "spaceship", "fuel", "asteroids_count", "asteroid_small", "asteroid_large",
           "bullets_count", "upcoming_asteroids_count", "upcoming_asteroid_small", "upcoming_asteroid_large"}
valid_key = {"width"}

df = open("examples/game_state_bad.txt", "r")
df = df.readlines()
df = df[0].split()

if (str(df[0]) not in {"width"}) or (str(df[0]) not in key_set):
    raise ValueError("Error: unexpected key {key} in line {line}".format(key=df[0], line=1))