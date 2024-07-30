import pygame, json, random
from ..utils.game_math import progression
from .typewriter import TypeWriter

class Settings():
  def __init__(self, font, game) -> None:
    self.path = "data\save\settings.json"
    self.controls_keyboard = {}
    self.display = {}
    self.record_time = {}
    self.font = font
    self.game = game
    self.curr_hover_pos = -1
    self.tab_hover_pos = 0
    self.typer = TypeWriter(font, (255,255,255), 200, 70, 600, 20, None)
    self.key_objs = []
    self.typer.write(["Hello World"])
    self.resolutions = [["Enter Full Screen", None, "NOT ADVISABLE! as may cause scalling issues Restart Required"], ["640x360", (640, 360), "640 x 360 Ideal for small screen devices Restart Required"], ["960x540", (960, 540), "960 x 540 Ideal for medium sized devices Restart Requried"], ["1280x720", (1280, 720), "1280 x 720 Highly Recommended for most high end monitors Restart Required"], ["1600x900", (1600, 900), "1600 x 900 May cause lags Restart Requried"], ["1920x1080", (1920, 1080), "1920 x 1080 May cause rendering lags Restart Requried"]]
    for x in range(len(self.resolutions)):
      self.resolutions[x].append(pygame.rect.Rect(10, 50 + x * 25, 150, 39))
      self.resolutions[x].append(pygame.rect.Rect(11, 50 + x * 25 + 3 , 146, 35))
      self.resolutions[x].append(False)
    
    # self.resolutions[random.randint(0,len(self.resolutions) - 1)][4] = True
    self.load()
    self.done_typing = False
  
  def default_conf(self):
    return {
      "controls_keyboard" : {
        "left" : [pygame.K_LEFT, pygame.K_a],
        "right" : [pygame.K_RIGHT, pygame.K_d],
        "up" : [pygame.K_UP, pygame.K_w],
        "down" : [pygame.K_DOWN, pygame.K_s],
        "jump" : [pygame.K_SPACE],
        "dash" : [pygame.K_l],
        "settings": [pygame.K_ESCAPE],
        "attack" : [pygame.K_j],
        "select" : [pygame.K_RETURN],
        "pickup" : [pygame.K_e]
      },
      "display" : {
        "res" : [960, 540]
      },
      "record_time":{
        "1": 0,
        "2" : 0,
        "3" : 0,
        "game" : 0,
      }
    }

  def convert_to_set(self, dict):
    return_dict = {}
    for key in dict.keys():
      return_dict[key] = set(dict[key]) 
    return return_dict
  
  def convert_to_dict(self, pdict):
    return_dict = {}
    for key in pdict.keys():
      return_dict[key] = list(pdict[key]) 
    return return_dict

  def update_res(self, new_res):
    self.display["res"] = new_res

  def load(self):
    try:
      file = open(self.path, "r")
      settings = json.load(file)
      file.close()
      self.controls_keyboard = self.convert_to_set(settings["controls_keyboard"])
      self.display = settings["display"]
      self.record_time = settings["record_time"]
    except:
      conf = self.default_conf()
      self.controls_keyboard = self.convert_to_set(conf["controls_keyboard"])
      self.display = conf["display"] 
      self.record_time = conf["record_time"]
    x = 0
    for key in self.controls_keyboard.keys():
      self.key_objs.append([key, pygame.rect.Rect(10, 50 + x * 25, 150, 39), pygame.rect.Rect(11, 50 + x * 25 + 3, 146, 35)])
      x += 1
    print(self.key_objs)
  
  def render(self, display, time):
    display.fill((0,0,0,0.5))
    #outline
    set_rect = pygame.rect.Rect(4, 4, progression(time, 1500, 90) , 30)
    controls_rect = pygame.rect.Rect(95, 4, progression(time, 1500, 90), 30)
    if self.tab_hover_pos == 0:
      pygame.draw.rect(display, (20,200,20), set_rect, border_bottom_right_radius=10)
      pygame.draw.rect(display, (200,200,200), controls_rect, border_bottom_right_radius=10)
    elif self.tab_hover_pos == 1:
      pygame.draw.rect(display, (200,200,200), set_rect, border_bottom_right_radius=10)
      pygame.draw.rect(display, (20,200,20), controls_rect, border_bottom_right_radius=10)
    #inner
    iset_rect = pygame.rect.Rect(5, 5, progression(time, 1000, 87), 26)
    pygame.draw.rect(display, (10,10,10), iset_rect, border_bottom_right_radius=10)
    icontrols_rect = pygame.rect.Rect(96, 5, progression(time, 1000, 87), 26)
    pygame.draw.rect(display, (10,10,10), icontrols_rect, border_bottom_right_radius=10)
    #typer
    img = self.font.render("Display", True, (255,255,255))
    display .blit(img, (14,4))
    img2 = self.font.render("Controls", True, (255,255,255))
    display.blit(img2, (98, 4))
    if self.tab_hover_pos == 0:
      self.render_settings(display, time)
    elif self.tab_hover_pos == 1:
      self.render_controls(display)
    display.set_colorkey((0,0,0,0))

  def update_hover_pos(self, offset):
    if self.tab_hover_pos == 0:
      self.curr_hover_pos  = (self.curr_hover_pos + offset) % len(self.resolutions)
    elif self.tab_hover_pos == 1:
      self.curr_hover_pos  = (self.curr_hover_pos + offset) % len(self.key_objs)
    self.done_typing = False
    self.typer.refresh()
    if self.tab_hover_pos == 0:
      self.typer.write([self.resolutions[self.curr_hover_pos][2],])

  def update_tab_hover_pos(self):
    self.tab_hover_pos = (self.tab_hover_pos + 1) % 2
    self.curr_hover_pos = -1
    self.done_typing = True
    self.typer.refresh()
  
  def render_settings(self, display, time):
    
    #Need to do more complicated calculations based on screen size.
    mouse_pos = list(pygame.mouse.get_pos())
    mouse_pos[0] /= 2
    mouse_pos[1] /= 2

    # self.curr_hover_pos = -1

    if pygame.display.is_fullscreen():
      self.resolutions[0][0] = "Windowed Mode"
    else:
      self.resolutions[0][0] = "Enter Full Screen"

    for pos, res in enumerate(self.resolutions):
      if pos != self.curr_hover_pos:
        pygame.draw.rect(display, (200,200,200), res[3], border_bottom_left_radius=10, border_top_right_radius=10)
        pygame.draw.rect(display, (10, 10,10), res[4], border_bottom_left_radius=9, border_top_right_radius=9)
        img = self.font.render(res[0], True, (255,255,255))
        display.blit(img, (res[3].x + 6, res[3].y + 2))
    
    if self.curr_hover_pos != -1:
      pygame.draw.rect(display, (10,200,10), self.resolutions[self.curr_hover_pos][3], border_bottom_left_radius=10, border_top_right_radius=10)
      pygame.draw.rect(display, (10, 10,10), self.resolutions[self.curr_hover_pos][4], border_bottom_left_radius=9, border_top_right_radius=9)
      img = self.font.render(self.resolutions[self.curr_hover_pos][0], True, (255,255,255))
      display.blit(img, (self.resolutions[self.curr_hover_pos][4].x + 6, self.resolutions[self.curr_hover_pos][4].y + 2))
    
    if not self.done_typing:
      self.done_typing = self.typer.update(time, display, [500,100])
  
  def render_controls(self, display):
    for pos, kobj in enumerate(self.key_objs):
      if pos != self.curr_hover_pos:
        pygame.draw.rect(display, (200,200,200), kobj[1], border_bottom_left_radius=10, border_top_right_radius=10)      
        pygame.draw.rect(display, (10, 10,10), kobj[2], border_bottom_left_radius=9, border_top_right_radius=9)
        img = self.font.render(kobj[0], True, (255,255,255))
        display.blit(img, (kobj[1].x + 6, kobj[1].y + 2))
    
    if self.curr_hover_pos != -1:
      pygame.draw.rect(display, (10,200,10), self.key_objs[self.curr_hover_pos][1], border_top_left_radius=10, border_top_right_radius=10)
      pygame.draw.rect(display, (10,10,10), self.key_objs[self.curr_hover_pos][2], border_top_left_radius=9, border_top_right_radius=9)
      img = self.font.render(self.key_objs[self.curr_hover_pos][0], True, (255,255,255))
      display.blit(img, (self.key_objs[self.curr_hover_pos][2].x + 6, self.key_objs[self.curr_hover_pos][2].y + 2))
    
    
      
    
    
  def save(self):
    file = open(self.path, "w")
    json.dump({"controls_keyboard" : self.convert_to_dict(self.controls_keyboard), "display" : self.display, "record_time": self.record_time}, file)
    file.close()
