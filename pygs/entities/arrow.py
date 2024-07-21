from pygs.entities.entity import PhysicsEntity
from pygs.ui.spark import Spark
import random, math

class Arrow(PhysicsEntity):
  def __init__(self, game, e_type, pos, size, gravity=False):
    super().__init__(game, e_type, pos, size, gravity)
    self.velocity = [0,4]
    self.timer = 0
    self.alive = True
    self.img = self.game.assets[e_type]
  
  def update(self, tilemap, movement, dt, gust):
    self.timer += 1
    super().update(tilemap, movement, dt, False)
    if self.timer > 360:
      self.alive = False
    if self.collisions['left'] or self.collisions['right'] or self.collisions['up'] or self.collisions['down']:
      #append sparks
      for x in range(4):
        self.game.sparks.append(Spark((self.pos[0] + self.size[0], self.pos[1] + self.size[1]),random.random() * -math.pi, 2 + random.random()))
      self.alive = False
    if self.velocity[0] > 0:
      self.velocity[0] = max(self.velocity[0] - 0.1, 0)
    else:
      self.velocity[0] = min(self.velocity[0] + 0.1, 0)
  
  def render(self, surf, offset = (0,0)):
    surf.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))

class ArrowManager():
  def __init__(self, loc, game) -> None:
    self.game = game
    self.loc = loc
    self.img = self.game.assets['machine']
  
  def update(self, threshold):
    if random.random() < threshold:
      self.shoot()
  
  def render(self, surf, offset=(0,0)):
    surf.blit(self.img, (self.loc[0] - offset[0], self.loc[1] - offset[1]))
  
  def shoot(self):
    self.game.arrows.append(Arrow(self.game, 'arrow', [self.loc[0] + 10, self.loc[1] + 5], (self.game.assets['arrow'].get_width(), self.game.assets['arrow'].get_height()), False))


