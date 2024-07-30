import math

def progression(time, cooldown, property):
  return int(min(time / cooldown, 1) * property)

def distance_between(pos1, pos2):
  return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def vector(pos1, pos2):
  return [pos2[0] - pos1[0], pos2[1] - pos1[1]]

def angle_between(vector):
  return math.atan2(vector[1], vector[0])

def magnitude(vector):
  return math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))

def normalise(vector):
  return [vector[0] / magnitude(vector), vector[1] / magnitude(vector)]

def convert_to_min_sec(time):
  min = time // 60
  sec = time % 60
  if len(str(sec)) == 1:
    sec = "0" + str(sec)
  return min, sec