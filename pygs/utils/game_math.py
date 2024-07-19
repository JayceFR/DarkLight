import math

def progression(time, cooldown, property):
  return int(min(time / cooldown, 1) * property)

def distance_between(pos1, pos2):
  return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)