from pygs.entities.entity import PhysicsEntity
import random, pygame, math
from pygs.utils.game_math import *
from pygs.ui.spark import Spark
from pygs.ui.particle import Particle

class Ghost(PhysicsEntity):
  def __init__(self, game, pos, size):
    super().__init__(game, 'ghost', pos, size, gravity=False)
    self.walking = 0
    self.angle = 0
    self.target_angle = 0
    self.pistol_flip = False
    self.alive = True
  
  def update(self, tilemap, movement=(0,0), dt=1, player_pos = (0,0)):
    super().update(tilemap, movement=movement, dt=dt, gravity=False)
  
  def render(self, surf, offset=(0,0)):
    surf.blit(self.game.assets[self.type], (self.pos[0] - offset[0], self.pos[1] - offset[1]))