import pygame, random, math

class Fireball():
  def __init__(self, game, pos, box = False, move_speed=5, cooldown = 10) -> None:
    self.pos = list(pos)
    self.game = game
    self.radius = 30
    self.cycle = 15
    self.box = box
    self.rect = pygame.rect.Rect(self.pos[0] - self.radius - 1, self.pos[1] - self.radius - 1, self.radius - 1, self.radius - 1)
    self.destination = {(pos[0], pos[1]), (pos[0] + self.cycle, pos[1]), (pos[0] + self.cycle, pos[1] + self.cycle), (pos[0], pos[1] + self.cycle)}
    self.vectors = [(0,1), (1,0), (0,-1), (-1,0)]
    self.curr_vector_pos = -1
    self.move_speed = move_speed
    self.last_update = 0
    self.angle = 0
    self.cooldown = cooldown
    self.animation = self.game.assets['fireball'].copy()
  
  def render(self, surf, offset):
    # pygame.draw.circle(surf, (255,0,0), (self.pos[0] - offset[0], self.pos[1] - offset[1]), self.radius)
    # pygame.draw.rect(surf, (0,0,255), (self.rect[0] - offset[0], self.rect[1] - offset[1], self.rect[2], self.rect[3]))
    surf.blit(self.animation.img(), (self.pos[0] - offset[0], self.pos[1]- offset[1]))
  
  def update(self, time):
    if time - self.last_update > self.cooldown:
      #time to switch
      self.angle = (self.angle + 5) % 360
      self.curr_vector_pos = (self.curr_vector_pos + 1) % len(self.vectors)
      self.last_update = time
    
    if self.box:
      self.pos[0] += self.vectors[self.curr_vector_pos][0] * self.move_speed
      self.pos[1] += self.vectors[self.curr_vector_pos][1] * self.move_speed
    else:
      self.pos[0] += math.cos(math.radians(self.angle)) * self.move_speed
      self.pos[1] += math.sin(math.radians(self.angle)) * self.move_speed
    
    self.rect = pygame.rect.Rect(self.pos[0] - self.radius//2 - 1, self.pos[1] - self.radius//2 - 1, self.radius - 1, self.radius - 1)
    self.animation.update()

