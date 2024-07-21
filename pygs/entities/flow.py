import pygame
from pygs.entities.arrow import Arrow

class Flow():
  def __init__(self, pos, size, game, e_type) -> None:
    self.pos = pos
    self.size = size
    self.game = game
    self.e_type = e_type
    self.img = self.game.assets['flow']
    self.rect = pygame.rect.Rect(pos[0], pos[1], size[0], size[1])
  
  def update(self):
    pass

  def render(self, surf, offset=(0,0)):
    surf.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
  
  def shoot(self):
    self.game.arrows.append(Arrow(self.game, self.e_type, [self.pos[0] + 15, self.pos[1] + 28], (self.game.assets[self.e_type].get_width(), self.game.assets[self.e_type].get_height()), False))
    


