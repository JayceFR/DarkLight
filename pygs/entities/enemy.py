from .entity import PhysicsEntity
import random, pygame, math
from pygs.utils.game_math import *

class Enemy(PhysicsEntity):
  def __init__(self, game, pos, size, pistol_img):
    super().__init__(game, 'enemy', pos, size)
    self.pistol_img = pistol_img
    self.walking = 0
    self.angle = 0
    self.target_angle = 0
    self.pistol_flip = False
  
  def update(self, tilemap, movement=(0,0), dt=1, player_pos = (0,0)):
    vec = vector((self.pos[0], -self.pos[1]), (player_pos[0], -player_pos[1]))
    abs_angle = angle_between( (abs(vec[0]), abs(vec[1])) )
    # print(math.degrees(abs_angle))
    self.target_angle = abs_angle
    if vec[0] < 0:
      if vec[1] > 0:
        self.target_angle = math.pi - abs_angle
      if vec[1] < 0:
        self.target_angle = -math.pi + abs_angle
    if vec[0] > 0:
      if vec[1] < 0:
        self.target_angle = -abs_angle
    # print(math.degrees(self.target_angle), vec)
    print(player_pos[0] - self.pos[0])
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
    
    if player_pos[0] > self.pos[0]:
      self.flip = False
    else:
      self.flip = True
    
    if math.degrees(self.angle) > 90 or math.degrees(self.angle) < -90:
      self.pistol_flip = True
    else:
      self.pistol_flip = False
  
  def render(self, surf, offset=(0,0)):
    super().render(surf, offset=offset)
    self.angle += (self.target_angle - self.angle) / 2
    pistol = self.pistol_img.copy()
    pistol = pygame.transform.flip(pistol, False, self.pistol_flip)
    pistol = pygame.transform.rotate(pistol, math.degrees(self.angle))
    surf.blit(pistol, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
  
class EnemyManager():
  def __init__(self, game, locs, size) -> None:
    self.game = game
    self.enemies = []
    for loc in locs:
      self.enemies.append(Enemy(game, loc, size, self.game.assets["pistol"]))
  
  def update(self, tilemap, display, scroll, dt):
    for enemy in self.enemies:
      dist_to_player = distance_between((enemy[0], enemy[1]), (self.game.player[0], self.game.player[1]))
      #if ditance is less than 40 or something then start shooting. 
      enemy.update(tilemap, (0,0), dt, (self.game.player[0], self.game.player[1]))
      enemy.render(display, offset=scroll)