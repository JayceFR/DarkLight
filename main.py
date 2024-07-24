import pygame, random, math
from pygame.locals import *
import pygs as pg

pygame.init()


'''
TODO 
The Assets for both characters
Enemies can shoot projectile to the player
Projectile collision and movement
Hyde's attack 
Need to remove the projectiles if they leave the screen
Map 
'''

class Game():
  def __init__(self):
    pygame.display.set_caption("DarkLight")
    self.settings = pg.Settings(pygame.font.Font('./data/font/munro.ttf', 20), self)
    flags = pygame.OPENGL | pygame.DOUBLEBUF
    if self.settings.display["res"] != None:
      SCREEN_WIDTH = self.settings.display["res"][0]
      SCREEN_HEIGHT = self.settings.display["res"][1]
    else:
      SCREEN_WIDTH = 1280
      SCREEN_HEIGHT = 720
    self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), flags )
    if self.settings.display["res"] == None:
      pygame.display.toggle_fullscreen()
    self.display = pygame.Surface((640,360))
    self.ui_display = pygame.Surface((640, 360), pygame.SRCALPHA)
    self.movement = [False, False]

    self.assets = {
      'player' : pg.load_img('entities/player/random.png', scale=1),
      'grass' : pg.load_imgs('tiles/grass', scale=1),
      'boomerang' : pg.load_img('entities/boomerang/0.png', scale=0.9),
      'decor': pg.load_imgs('tiles/decor', scale=1, color_key=(255,255,255), args={'tree3.png':[1.5,None], 'tree4.png':[1.5,None]}),
      'stone': pg.load_imgs('tiles/stone', scale=1),
      'snow' : pg.load_imgs('tiles/snow', scale=1),
      'spike':pg.load_imgs('tiles/spike', scale=1),
      'lamp': pg.load_imgs('tiles/lamp', scale=2, color_key=(255,255,255)),
      'flower': pg.load_imgs('tiles/flower', (255,255,255)),
      'bullet': pg.load_img('entities/enemy/bullet.png', (0,0,0), 1),
      'machine': pg.load_img('ui/machine.png', scale=1.5),
      'arrow': pg.load_img('ui/arrow.png', scale=2),
      'ball' : pg.load_img('ui/ball.png', scale=1),
      'citizen/idle' : pg.Animation(pg.load_imgs('entities/citizen/idle'), img_dur=15),
      'citizen/run': pg.Animation([pg.load_img('entities/citizen/player3.png', scale=1, color_key=(255,255,255)),],),
      'enemy/idle' : pg.Animation(pg.load_imgs('entities/enemy/idle', scale=0.8), img_dur=15),
      'enemy/run': pg.Animation(pg.load_imgs('entities/enemy/run', scale=0.8), img_dur=10),
      'flow' : pg.load_img('ui/flow.png'),
      'pistol' : pg.load_img('entities/enemy/pistol.png', (0,0,0)),
      'player/idle' : pg.Animation(pg.load_imgs('entities/player/idle', scale=1, color_key=(255,255,255)), img_dur=10),
      'player/run' : pg.Animation(pg.load_imgs('entities/player/run', scale=1, color_key=(255,255,255)), img_dur=6),
      'player/jump': pg.Animation(pg.load_imgs('entities/player/jump', scale=1, color_key=(0,0,0))),
      'player/hit' : pg.Animation(pg.load_imgs('entities/player/hit', scale=1), img_dur=6),
      'player/climb' : pg.Animation(pg.load_imgs('entities/player/climb', scale=1)),
      'player/hit_up': pg.Animation(pg.load_imgs('entities/player/hit_up', scale=1), img_dur=6),
      'player/death': pg.Animation(pg.load_imgs('entities/player/death', scale=1), img_dur=6, loop=False),
      'player/hit_down': pg.Animation(pg.load_imgs('entities/player/hit_down', scale=1), img_dur=6),
      'particles/particle' : pg.Animation(pg.load_imgs('particle', scale=2), img_dur=6, loop=False),
      'player/speak' : pg.Animation(pg.load_imgs('entities/player/speak', scale=5), img_dur=16),
      'citizen/speak' : pg.Animation(pg.load_imgs('entities/citizen/speak', scale=5), img_dur=16),
      'ghost' : pg.load_img('ui/ghost.png'),
      'eyeball' : pg.load_img('ui/eyeball.png', scale=5),
      'potion' : pg.load_img('ui/potion.png', scale=5),
      'skull' : pg.load_img('ui/skull.png', scale=5),
    }

    self.sfx = {
      'ambience': pygame.mixer.Sound('./data/music/ambience.wav'),
      'song': pygame.mixer.Sound('./data/music/song.wav'),
      'jump': pygame.mixer.Sound('./data/music/jump.wav'),
      'pickup' : pygame.mixer.Sound('./data/music/pickup.wav')
    }

    self.sfx['ambience'].set_volume(0.05)
    self.sfx['song'].set_volume(0.7)
    self.sfx['jump'].set_volume(0.1)

    self.hud = pg.ui.Hud(self)

    pygame.key.set_mods(0)

    self.clock = pygame.time.Clock()
    self.player = pg.entities.Player(self, [0,0], [self.assets['player'].get_width(),self.assets['player'].get_height()])
    # self.player = Player(self, [0,0], [12,])

    self.dt = 0

    self.tilemap = pg.TileMap(self, tile_size=16)
    self.curr_level = 0 

    self.levels = [
      ["map", "j", ["These Hoodie Reddies constantly bully us", "Oh yeah i fugured it out", "What harm did we do? Hope my dear friend is safe", "Only if we had the strength to face them.", "Yeah, i feel helpless and abandoned"], 'eyeball', (586, 602)],
      ["1", "h"],
      ["map", "j", ["Oh praise the lord, You brought the second ingredient", "Thanks I guess... It is not too dangerous out there", "Wait do you not know", "Umm... What", "Yesterday someone took down some of the red hoodies", "Oh a saviour finally", "Take some rest now, Good night", "Good night"], 'potion', (137, 170)], 
      ["2", "h"],
      ["map", "j", ["Thanks for bringing the last ingredient!", "Your welcome", "You have done a really good job but I can offer nothing in return except this shed", "That's more than enough for me, now the real threat arises",], 'skull', (383, 874)], 
      ["3", "h"],
    ]

    # self.levels = [
    #   ["map", "h"]
    # ]

    self.load_level(
      self.levels[self.curr_level]
    )
  
  #level -> [name, j/h, list_of_text]
  def load_level(self, level):
    print(level)
    self.tilemap.load('data/save/maps/' + level[0] + '.json')
    # self.tilemap.load('./map.json')

    self.player.who = level[1]

    if self.player.who == "j":
      self.font = pygame.font.Font('./data/font/munro.ttf', 20)
      self.typer = pg.TypeWriter(self.font, (255,255,255), 150,70, 600, 20, None)
      self.player_talk = self.assets['player/speak'].copy()
      self.citizen_talk = self.assets['citizen/speak'].copy()
      self.typer.write(level[2])
      self.buried_point = level[4]
      self.img = self.assets[level[3]]
      self.close_to_point = False
      self.done_typing = False
      self.collected = False
      self.delivered = False
      self.home_pos = [1025, 938]

    self.dimension = [82,61]

    self.fragment_loc = "./data/scripts/fragment.frag"
    self.vertex_loc = "./data/scripts/vertex.vert"
    self.noise_img1 = pygame.image.load('./data/images/misc/pnoise.png').convert_alpha()
    self.noise_img2 = pygame.image.load('./data/images/misc/pnoise2.png').convert_alpha()
    self.shader_obj = pg.Shader(True, self.vertex_loc, self.fragment_loc)

    flower_objs = self.tilemap.get_objs('flower')
    self.flower = pg.entities.Flowers(flower_objs, self.assets, self)
    self.gust = pg.entities.Gust(self)

    self.scroll = []

    self.citizens = []
    self.water_pos = []
    self.fire_pos = []
    self.enemy_locs = []
    self.flows = []
    self.machines = []
    self.ghost = []

    self.sparks = []

    for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1), ('spawners', 2), ('spawners', 3), ('spawners', 4), ('spawners', 5), ('spawners', 6)]):
      if spawner['variant'] == 0:
        self.player.pos = spawner['pos']
      elif spawner['variant'] == 1:
        self.citizens.append(pg.entities.Citizen(self, spawner['pos'], (12,29)))
      elif spawner['variant'] == 2:
        self.water_pos.append(spawner['pos'])
      elif spawner['variant'] == 3:
        self.enemy_locs.append(spawner['pos'])
      elif spawner['variant'] == 4:
        self.flows.append(pg.entities.Flow(spawner['pos'], (self.assets['flow'].get_width(), self.assets['flow'].get_height()), self, 'ball'))
      elif spawner['variant'] == 5:
        self.machines.append(pg.entities.ArrowManager(spawner['pos'], self))
      elif spawner['variant'] == 6:
        self.ghost.append(pg.entities.Ghost(self, spawner['pos'], (self.assets['ghost'].get_width(), self.assets['ghost'].get_height()) ))
    
    self.water_manager = pg.ui.WaterManager()
    self.water_manager.load(self.water_pos, self)
    for fire_pos in self.tilemap.extract([('decor', 4),], True):
      self.fire_pos.append(fire_pos)

    self.glow_img = pygame.Surface((255,255))
    self.glow_img.fill((174*0.2, 226*0.2, 255*0.3))
    img = pygame.image.load('./data/images/misc/light.png').convert()
    self.glow_img.blit(img, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    self.fireflies = pg.ui.Fireflies(self.display.get_width(),self.display.get_height(), self.glow_img)

    self.pglow_img = pygame.Surface((255,255))
    self.pglow_img.fill((255*0.2, 183*0.2, 255*0.3))
    self.pglow_img.blit(img, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    self.fireflies = pg.ui.Fireflies(self.display.get_width(),self.display.get_height(), self.glow_img)

    self.lamp_img = pygame.Surface((730, 1095))
    self.lamp_img.fill((255*0.6, 255*0.6, 255*0.6))
    lamp_img = pygame.image.load('./data/images/misc/lamp2.png').convert()
    self.lamp_img.blit(lamp_img, (0,0), special_flags=BLEND_RGBA_MULT)
    self.lamp_glow_img = pygame.Surface((255,255))
    self.lamp_glow_img.fill((255*0.3, 255*0.3, 255*0.3))
    self.lamp_glow_img.blit(img, (0,0), special_flags=BLEND_RGBA_MULT)
    self.lamp_glow_img = pygame.transform.scale(self.lamp_glow_img, (60,60))
    self.lamp_img = pygame.transform.scale(self.lamp_img, (self.lamp_img.get_width()//10, self.lamp_img.get_height()//10))

    self.lamp_positions = []
    for lamp_pos in self.tilemap.extract([('lamp',0),], True):
      self.lamp_positions.append(lamp_pos)

    leaf_img = pygame.image.load('./data/images/ui/leaf.png').convert()
    leaf_img.set_colorkey((0,0,0))
    self.leaf = pg.ui.LeafManager(self.display.get_width(), self.display.get_height(), leaf_img )
    
    self.particles = []
    self.arrows = []
    self.enemy = pg.entities.EnemyManager(self, self.enemy_locs, (20 * 0.8,38 * 0.8))
    self.screenshake = 0

    self.true_scroll = [0,0]
    self.full_screen = False
    self.fire_particles = []
    for obj in self.fire_pos:
      self.fire_particles.append(pg.ui.Flame((obj['pos'][0] + 10, obj['pos'][1] + 2)))
    # self.scroll = [0,0]
    self.settings_window = False
    self.darkness = 0

    self.dead = -3
    self.transition = -30

  @pg.pygs
  def run(self):
      self.clock.tick(60)
      if self.dead > 0:
        self.dead += 1
        if self.dead >= 50:
          self.transition = min(self.transition + 1, 30)
        if self.dead > 80:
          self.load_level(self.levels[self.curr_level])

      if self.player.who == "h":
        if len(self.enemy.enemies) == 0 and len(self.ghost) == 0:
          self.transition += 1

      if self.transition > 30:
        self.curr_level += 1
        self.load_level(self.levels[self.curr_level])
        
      time = pygame.time.get_ticks()
      # print(self.clock.get_fps())
      self.ui_display.fill((0,0,0,0))
      self.display.fill((2,2,2))

      if self.transition < 0:
        self.transition += 1

      self.screenshake = max(0, self.screenshake - 1)

      controls = self.hud.get_controls()
      if self.dead <= 0:
        self.movement = [False, False]
        if not self.settings_window:
          if controls['left'] :
            self.movement[0] = True
          if controls['right']:
            self.movement[1] = True

      self.true_scroll[0] += (self.player.rect().x - self.true_scroll[0] - 1280//4) / 5
      self.true_scroll[1] += (self.player.rect().y - self.true_scroll[1] - 720//4) / 20

      self.true_scroll[0] = max(0, min( self.dimension[0] * self.tilemap.tile_size - self.display.get_width(), self.true_scroll[0] ))
      self.true_scroll[1] = max(0, min(self.dimension[1] * self.tilemap.tile_size - self.display.get_height(), self.true_scroll[1] ))

      self.scroll = self.true_scroll.copy()
      self.scroll[0] = int(self.scroll[0])
      self.scroll[1] = int(self.scroll[1])

      self.tilemap.render(self.display, self.scroll)

      self.flower.update(self.player.rect(), self.display, self.scroll, time, self.gust.wind())

      for citizen in self.citizens:
        citizen.update(self.tilemap, (0,0), self.dt)
        citizen.render(self.display, offset=self.scroll)
      
      for machine in self.machines:
        machine.update(0.01)
        machine.render(self.display, self.scroll)
      
      for ghost in self.ghost:
        ghost.update(self.tilemap)
        ghost.render(self.display, self.scroll)
      
      for arrow in self.arrows.copy():
        if not arrow.alive:
          self.arrows.remove(arrow)
        else:
          arrow.update(self.tilemap, (0,0), self.dt, self.gust.wind())
          arrow.render(self.display, self.scroll)
          if arrow.rect().colliderect(self.player.rect()) and abs(self.player.dashing[1]) < 30 and abs(self.player.dashing[0]) < 30:
            arrow.alive = False
            self.screenshake = max(16, self.screenshake)
            for x in range(30):
              angle = random.random() * math.pi * 2
              speed = random.random() * 5
              self.sparks.append(pg.ui.Spark(self.player.rect().center, angle, 2 + random.random()))
              self.particles.append(pg.ui.Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5 ], frame=random.randint(0,7)))
      
      self.enemy.update(self.tilemap, self.display, self.scroll, self.dt)

      for flow in self.flows.copy():
        flow.render(self.display, self.scroll)
        if random.random() < 0.005:
          flow.shoot()
        if flow.rect.colliderect(self.player.rect()):
          self.player.pos[0] = flow.rect.center[0] - 9
          self.player.pos[1] = flow.rect.center[1] - 9
          #give them an extra dash if they don't have one
          self.player.dashes = 1
          self.player.velocity[1] = 0
          #if player hits remove flow
          if self.player.hit:
            self.flows.remove(flow)

      self.player.update(self.tilemap, [self.movement[1] - self.movement[0], 0], self.dt, self.gust.wind())
      self.player.render(self.display, self.scroll)
      self.display.blit(self.pglow_img, (self.player.rect().center[0] - 255 //2 - self.scroll[0] , self.player.rect().center[1] - 255//2 - self.scroll[1] ), special_flags=BLEND_RGBA_ADD)


      for particle in self.fire_particles:
        particle.draw_flame(self.display, self.scroll)

      self.water_manager.update(self)


      if self.settings_window:
        self.settings.render(self.ui_display, time)
      
      #lamp img 
      for lamp in self.lamp_positions:
        pos = lamp['pos']
        self.display.blit(self.lamp_img, (pos[0] - self.scroll[0] - 24, pos[1] - self.scroll[1] + 30), special_flags=BLEND_RGBA_ADD)
        self.display.blit(self.lamp_glow_img, (pos[0] - self.scroll[0] - 17, pos[1] - self.scroll[1] - 10), special_flags=BLEND_RGBA_ADD)

      self.gust.update(time)

      for spark in self.sparks.copy():
        kill = spark.update()
        spark.render(self.display, self.scroll, self.dt)
        if kill:
          self.sparks.remove(spark)

      self.fireflies.recursive_call(time, self.display, self.scroll, self.dt)
      self.leaf.recursive_call(time, self.display, self.scroll, self.gust.wind(), dt=self.dt)

      if self.player.who == "j":
        if self.delivered:
          if not self.done_typing:
            pygame.draw.rect(self.ui_display, (0,0,0), pygame.rect.Rect(0,0, 640, 180))
            self.done_typing = self.typer.update(time, self.ui_display, enter_loc=(350,300))
            if self.typer.banana_turn % 2 != 0:
              self.ui_display.blit(self.player_talk.img(), (10,10))
              self.player_talk.update()
            else:
              self.ui_display.blit(self.citizen_talk.img(), (10,10))
              self.citizen_talk.update()
          else:
            self.transition += 1

        if not self.collected:
          if self.player.rect().collidepoint(self.buried_point[0], self.buried_point[1]):
            #draw E
            img = self.font.render("E To Collect", False, (255,255,255))
            self.ui_display.blit(img, (500, 330))
        
        if self.collected and not self.delivered:
          if self.player.rect().collidepoint(self.home_pos[0], self.home_pos[1]):
            img = self.font.render("E To Deliver", False, (255,255,255))
            self.ui_display.blit(img, (500, 330))
        
        if self.collected and not self.delivered:
          self.ui_display.blit(self.img, (10,10))

      self.hud.events(self.settings.controls_keyboard)
      

Game().run()
