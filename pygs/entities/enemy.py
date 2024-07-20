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
  
class Projectile(PhysicsEntity):
  def __init__(self, game, e_type, pos, size, img, init_velocity, angle_of_rot):
    super().__init__(game, e_type, pos, size, False)
    self.img = pygame.transform.rotate(img, math.degrees(angle_of_rot))
    self.alive = True
    self.velocity = init_velocity
  
  def update(self, tilemap, movement=(0,0), dt=1):
    super().update(tilemap, movement, dt, gravity=False)
    if self.collisions["left"] or self.collisions["right"] or self.collisions["up"] or self.collisions["down"]:
      self.alive = False
  
  def render(self, surf, offset=(0,0)):
    surf.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
    

  
class EnemyManager():
  def __init__(self, game, locs, size) -> None:
    self.game = game
    self.enemies = []
    self.projectiles = []
    self.positive_range = [0.2, 0.3, 0, 0, 0.5, 0.5, 0.7]
    self.negative_range = [-0.2, -0.3, 0, 0, -0.5, -0.5, -0.7]
    for loc in locs:
      self.enemies.append(Enemy(game, loc, size, self.game.assets["pistol"]))
  
  def update(self, tilemap, display, scroll, dt):
    for enemy in self.enemies:
      dist_to_player = distance_between((enemy[0], enemy[1]), (self.game.player[0], self.game.player[1]))
      #if ditance is less than 40 or something then start shooting. 
      enemy.update(tilemap, (0,0), dt, (self.game.player[0], self.game.player[1]))
      enemy.render(display, offset=scroll)
      if dist_to_player < 250:
        if random.random() <= 0.02:
          vec = enemy.vec
          vec[1] *= -1
          nvec = normalise(vec)
          xrange = self.positive_range
          yrange = self.positive_range
          if nvec[0] < 0:
            xrange = self.negative_range
          if nvec[1] < 0:
            yrange = self.negative_range
          nvec[0] = nvec[0] + random.choice(xrange) * 20
          nvec[1] = nvec[1] + random.choice(yrange) * 20
          self.projectiles.append(Projectile(self.game, 'bullet', (enemy[0], enemy[1]), (self.game.assets['bullet'].get_width(), self.game.assets['bullet'].get_height()), self.game.assets['bullet'], nvec, enemy.target_angle))
    
    for projectile in self.projectiles.copy():
      if not projectile.alive:
        self.projectiles.remove(projectile)
      else:
        projectile.update(tilemap, (0,0), dt)
        projectile.render(display, scroll)
        if projectile.rect().colliderect(self.game.player.rect()):
          self.projectiles.remove(projectile)
