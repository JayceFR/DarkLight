from .entity import PhysicsEntity
import random
from pygs.utils.game_math import *

class Enemy(PhysicsEntity):
  def __init__(self, game, pos, size):
    super().__init__(game, 'enemy', pos, size)

    self.walking = 0
  
  def update(self, tilemap, movement=(0,0), dt=1):
    if self.walking:
      if tilemap.solid_check((self.rect().centerx + (-self.size[0]//2 if self.flip else self.size[0]//2), self.pos[1] + self.size[1])):
        if (self.collisions['right'] or self.collisions['left']):
          self.flip = not self.flip
        else:
          movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
      else:
        self.flip = not self.flip
      self.walking = max(0, self.walking-1)
    elif random.random() < 0.01:
      self.walking = random.randint(30,120)
    
    super().update(tilemap, movement=movement, dt=dt)

    if movement[0] != 0:
      self.set_action('run')
    else:
      self.set_action('idle')
  
class EnemyManager():
  def __init__(self, game, locs, size) -> None:
    self.game = game
    self.enemies = []
    for loc in locs:
      self.enemies.append(Enemy(game, loc, size))
  
  def update(self, tilemap, display, scroll, dt):
    for enemy in self.enemies:
      dist_to_player = distance_between((enemy[0], enemy[1]), (self.game.player[0], self.game.player[1]))
      #if ditance is less than 40 or something then start shooting. 
      enemy.update(tilemap, (0,0), dt)
      enemy.render(display, offset=scroll)