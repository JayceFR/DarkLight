import random, pygame, math
from pygs.utils.game_math import *
from pygs.ui.spark import Spark
from pygs.ui.particle import Particle
from pygs.entities.enemy import Projectile

class Ghost():
  def __init__(self, game, pos, size, e_manager):
    self.pos = pos
    self.game = game
    self.type = "ghost"
    self.size = size
    self.e_manager = e_manager
    self.walking = 0
    self.proj_speed = 5
    self.movement_speed = 5
    self.attacking = 0
    self.alive = True
    self.flip = False
    self.health = 100
    self.rect = pygame.rect.Rect(pos[0], pos[1], size[0], size[1])
    self.vec_list = [(1,0), (-1,0), (0,1), (0,-1), (0.5, 0.5), (-0.5, 0.5), (0.5, -0.5), (-0.5, -0.5)]
  
  def update(self, player_pos = (0,0), dt=1):
    # print(distance_between(self.pos, player_pos))
    self.vec = vector((self.pos[0], -self.pos[1]), (player_pos[0], -player_pos[1]))
    abs_angle = angle_between( (abs(self.vec[0]), abs(self.vec[1])) )
    # print(math.degrees(abs_angle))
    self.target_angle = abs_angle
    if self.vec[0] < 0:
      if self.vec[1] > 0:
        self.target_angle = math.pi - abs_angle
      if self.vec[1] < 0:
        self.target_angle = -math.pi + abs_angle
    if self.vec[0] > 0:
      if self.vec[1] < 0:
        self.target_angle = -abs_angle
    
    if self.pos[0] < player_pos[0]:
      self.flip = True
    else:
      self.flip = False
    
    self.vec[1] *= -1
    nvec = normalise(self.vec)
    
    if not self.attacking:
      if distance_between(self.pos, player_pos) > 200:
        self.pos[0] += nvec[0] 
        self.pos[1] += nvec[1]
      else:
        self.attacking = 190
        for vec in self.vec_list:
          vec_copy = [vec[0] * self.proj_speed, vec[1] * self.proj_speed]
          self.e_manager.projectiles.append(Projectile(self.game, 'bullet', [self.pos[0] + self.size[0] //2 , self.pos[1] + self.size[1] // 2], (self.game.assets['bullet'].get_width(), self.game.assets['bullet'].get_height()), self.game.assets['bullet'], vec_copy, self.target_angle ))

    self.attacking = max(0, self.attacking - 1)
    self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    #check for collisions with the player
    if self.game.player.hit and self.game.player.get_hit_rect().colliderect(self.rect):
      self.game.screenshake = 14
      for x in range(5):
        angle = random.random() * math.pi * 2
        self.game.sparks.append(Spark(self.rect.center, angle, 3 + random.random()))
      self.health -= 1
    
    if self.health <= 0:
      self.game.sparks.append(Spark(self.rect.center, 0, 5 + random.random()))
      self.game.sparks.append(Spark(self.rect.center, math.pi, 5 + random.random()))
      self.alive = False
  
  def render(self, surf, offset=(0,0)):
    surf.blit(pygame.transform.flip(self.game.assets[self.type], self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))