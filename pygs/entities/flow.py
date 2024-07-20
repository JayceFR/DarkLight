import pygame

class Flow():
  def __init__(self, pos, size, game) -> None:
    self.pos = pos
    self.size = size
    self.game = game
    self.img = self.game.assets['flow']
    self.rect = pygame.rect.Rect(pos[0], pos[1], size[0], size[1])
  
  def update(self):
    pass

  def render(self, surf, offset=(0,0)):
    surf.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
    


