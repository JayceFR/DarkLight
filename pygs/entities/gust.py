import random
class Gust:
  def __init__(self,game) -> None:
    self.gust = 0
    self.target_gust = 0
    self.game = game
    self.gust_choice = [-40, -20, 0, 0, 0, 20, 40]
    self.gust_update_cooldown = 4000
    self.gust_last_update = 0
  
  def update(self, time):
    #update gust
    self.gust += (self.target_gust - self.gust) // 3
    if time - self.gust_last_update > self.gust_update_cooldown:
      if self.target_gust < 0 or self.target_gust > 0:
        if self.game.player.last_movement[0] > 0 and self.target_gust * -1 < 0:
          self.game.player.max_speed[0] = self.game.player.orig_max_speed[0]
        if self.game.player.last_movement[0] < 0 and self.target_gust * -1 > 0:
          self.game.player.max_speed[1] = self.game.player.orig_max_speed[1]
        self.target_gust = 0
        if random.randint(0,3) == 0:
          self.gust = 0
      else:
        self.target_gust = self.gust_choice[random.randint(0, len(self.gust_choice)-1)]
        self.game.player.velocity[0] += self.target_gust * -0.01
        if self.target_gust * -0.1 > 0:
          self.game.player.max_speed[1] = min(self.game.player.max_speed[1] + abs(self.target_gust * -0.1), 9)
          self.game.player.max_speed[0] = self.game.player.orig_max_speed[0]
        if self.target_gust * -0.1 < 0:
          self.game.player.max_speed[0] = min(self.game.player.max_speed[0] + abs(self.target_gust * -0.1), 9)
          self.game.player.max_speed[1] = self.game.player.orig_max_speed[1]
      self.gust_last_update = time
  
  def wind(self):
    return self.gust