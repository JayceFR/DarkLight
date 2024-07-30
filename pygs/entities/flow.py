import pygame
from pygs.entities.arrow import Arrow

class Flow():
  def __init__(self, pos, size, game, e_type) -> None:
    self.pos = pos
    self.size = size
    self.game = game
    self.e_type = e_type
    self.last_shoot = 0
    self.img = self.game.assets['flow']
    self.animation = self.game.assets['flow_ani'].copy()
    self.rect = pygame.rect.Rect(pos[0], pos[1], size[0], size[1])
  
  def update(self):
    self.animation.update()

  def render(self, surf, offset=(0,0)):
    surf.blit(self.animation.img(), (self.pos[0] - offset[0], self.pos[1] - offset[1]))
  
  def shoot(self):
    self.game.arrows.append(Arrow(self.game, self.e_type, [self.pos[0] + 35, self.pos[1] + 13], (self.game.assets[self.e_type].get_width(), self.game.assets[self.e_type].get_height()), False, velocity=[7,0]))
    self.game.arrows.append(Arrow(self.game, self.e_type, [self.pos[0] - 5, self.pos[1] + 13], (self.game.assets[self.e_type].get_width(), self.game.assets[self.e_type].get_height()), False, velocity=[-7,0]))

    


