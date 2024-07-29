import pygame, random, math
from pygame.locals import *
import pygs as pg

pygame.init()


'''
TODO 
Map levels
If we have time then have an attack cooldown which does 
allow the player to get killed in a second

Transition sound effect
Hit sound effect
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
      'hsnow' : pg.pallete_swap_imgs(
        'tiles/snow', 
        [[(153,217,234), (87,18,27)],
         [(255,255,255), (87,40,55)],
         [(168,73,121), (136,0,21)],
         [(255,174,201), (237,28,36)]
         ], 
        scale=1
      ),
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
      'jplayer/idle' : pg.Animation(pg.load_imgs('entities/player/idle', scale=1, color_key=(255,255,255)), img_dur=10),
      'hplayer/idle' : pg.Animation(pg.load_imgs('entities/player/hidle', scale=1, color_key=(255,255,255)), img_dur=10),
      'jplayer/run' : pg.Animation(pg.load_imgs('entities/player/run', scale=1, color_key=(255,255,255)), img_dur=6),
      'hplayer/run' : pg.Animation(pg.load_imgs('entities/player/hrun', scale=1, color_key=(255,255,255)), img_dur=6),
      'jplayer/jump': pg.Animation(pg.load_imgs('entities/player/jump', scale=1, color_key=(0,0,0))),
      'hplayer/jump': pg.Animation(pg.load_imgs('entities/player/hjump', scale=1, color_key=(0,0,0))),
      'jplayer/hit' : pg.Animation(pg.load_imgs('entities/player/hit', scale=1), img_dur=6),
      'hplayer/hit' : pg.Animation(pg.load_imgs('entities/player/hhit', scale=1), img_dur=6),
      'jplayer/climb' : pg.Animation(pg.load_imgs('entities/player/climb', scale=1)),
      'hplayer/climb' : pg.Animation(pg.load_imgs('entities/player/hclimb', scale=1)),
      'jplayer/hit_up': pg.Animation(pg.load_imgs('entities/player/hit_up', scale=1), img_dur=6),
      'hplayer/hit_up': pg.Animation(pg.load_imgs('entities/player/hhit_up', scale=1), img_dur=6),
      'jplayer/death': pg.Animation(pg.load_imgs('entities/player/death', scale=1), img_dur=6, loop=False),
      'hplayer/death': pg.Animation(pg.load_imgs('entities/player/hdeath', scale=1), img_dur=6, loop=False),
      'jplayer/hit_down': pg.Animation(pg.load_imgs('entities/player/hit_down', scale=1), img_dur=6),
      'hplayer/hit_down': pg.Animation(pg.load_imgs('entities/player/hhit_down', scale=1), img_dur=6),
      'particles/particle' : pg.Animation(pg.load_imgs('particle', scale=2), img_dur=6, loop=False),
      'player/speak' : pg.Animation(pg.load_imgs('entities/player/speak', scale=5), img_dur=16),
      'citizen/speak' : pg.Animation(pg.load_imgs('entities/citizen/speak', scale=5), img_dur=16),
      'cage' : pg.Animation(pg.load_imgs('entities/bro/cage', scale=1), img_dur=1, loop=False), 
      'ghost' : pg.load_img('ui/ghost.png'),
      'eyeball' : pg.load_img('ui/eyeball.png', scale=5),
      'potion' : pg.load_img('ui/potion.png', scale=5),
      'skull' : pg.load_img('ui/skull.png', scale=5),
      'fireball': pg.Animation(pg.load_imgs('ui/fireball', color_key=(0,0,0), scale=0.1), img_dur=3),
      'heart': pg.load_img('ui/heart.png', scale=1),
      'flash' : pg.Animation(pg.load_imgs('ui/flash', scale=1), img_dur=5, loop=False),
      'bro': pg.load_img('entities/bro/bro.png', scale=1),
      'story' : pg.load_img('ui/story.png', scale=3)
    }

    self.sfx = {
      'ambience': pygame.mixer.Sound('./data/music/ambience.wav'),
      'sparkle': pygame.mixer.Sound('./data/music/sparkle.wav'), 
      'song': pygame.mixer.Sound('./data/music/song.wav'),
      'jump': pygame.mixer.Sound('./data/music/jump.wav'),
      'pickup' : pygame.mixer.Sound('./data/music/pickup.wav'),
      'dash': pygame.mixer.Sound('./data/music/dash.wav'),
      'attack' : pygame.mixer.Sound('./data/music/attack.wav'),
      'run' : pygame.mixer.Sound('./data/music/run.wav'),
      'death': pygame.mixer.Sound('./data/music/death.wav')
    }

    self.sfx['ambience'].set_volume(0.05)
    self.sfx['sparkle'].set_volume(0.05)
    self.sfx['song'].set_volume(0.5)
    self.sfx['jump'].set_volume(0.3)
    self.sfx['run'].set_volume(0.5)
    self.sfx['dash'].set_volume(0.3)
    self.sfx['attack'].set_volume(0.3)
    self.sfx['death'].set_volume(0.2)

    self.hud = pg.ui.Hud(self)

    pygame.key.set_mods(0)

    self.clock = pygame.time.Clock()
    self.player = pg.entities.Player(self, [0,0], [self.assets['player'].get_width(),self.assets['player'].get_height()])
    # self.player = Player(self, [0,0], [12,])

    self.dt = 0

    self.tilemap = pg.TileMap(self, tile_size=16)
    self.curr_level = 1 
    self.curr_world = 0

    self.max_hearts = -10

    self.story_cooldown = 300

    self.scroll = []

    self.tutorial_text = ["The city of darklight is a mysterious and dangerous place", "But it does look quite beautiful", "Try making it home before its too late", "Too late for what", "For Overheat", "Overheat?", "No one has ever survived the overheat.", "What happens when one is overheated", "Legends has it that one sees the true nature of darklight"]
    level_one_text = ["Oh you have survived the day, I thought you wouldn't", "...", "What brings you here", "Hmm.. hiking", "No one visits the ruins of darklight for hiking, stop lying", "Few days ago my brother visited this place on his geography trip", "Oh yeah I did see some school students, I did warn them ", "He never returned, so I am looking for him ", "I am really sorry, but I believe he is captured by the red hoodies", "The red what?", "They are a ruthless tribe who flourish in this ruined city.", "Oh!!", "They are the ones who cursed this beautiful place with overheat", "Oh it must be them, they captured my little brother", "Enough talk lets take some rest, don't want to get overheated"]
    level_two_text = ["Oh hi there", "I found my brother's cap I believe I am in the right path", "Wait were you just overheated", "Yeah I guess so ", "Only the descendants of the king of shadows can survive in the overheated state", "My great-grandfather was no king of shadows", "Wait is it true that you saw a ghost", "Yeah it almost got me", "The ghosts are the spirits of the lost souls who perished overheated", "Is there a way to restore this place ", "Legend has it that the only true descendent of the king of the shadows can restore this place.", "Oh", "Lest's take some rest now"]
    self.game_over_text = ["You sacrificed your life for saving your brother and the village", "You are our hero", "We can't thank you enough"]
    self.world = {
      #  [max_level, list_of_texts]
      0: [1, self.tutorial_text],
      1: [2, level_one_text],
      2: [2, level_two_text],
      3: [2, []]
    }

    # self.levels = [
    #   ["map", "h"]
    # ]

    self.player.update_who("j")

    self.start_time = 0
    self.load_level(
      self.world[self.curr_world]
    )

    # self.load_level(level=None, text=self.world[self.curr_world][1])
  
  #level -> [name, j/h, list_of_text]
  def load_level(self, level=None, text=[]):
    print(level)
    if level:
      self.tilemap.load('data/save/maps/world' + str(self.curr_world) + "/" + str(self.curr_level) + '.json')
    else:
      self.tilemap.load('data/save/maps/home/map.json')

    # self.player.who = level[1]

    self.flow_shoot_cooldown = random.randint(800,1200)

    self.font = pygame.font.Font('./data/font/munro.ttf', 20)
    self.typer = pg.TypeWriter(self.font, (255,255,255),150,70, 900, 20, None)
    self.player_talk = self.assets['player/speak'].copy()
    self.citizen_talk = self.assets['citizen/speak'].copy()
    self.typer.write(text)
    self.done_typing = False
    self.home_pos = [530, 218]
    self.home_rect = pygame.rect.Rect(self.home_pos[0], self.home_pos[1], 32,16)

    self.game_over_typer =  pg.TypeWriter(self.font, (255,255,255),150,70, 900, 20, None)
    self.game_over_typer.write(self.game_over_text)
    self.game_over_typing = False

    self.dimension = [82,61]

    self.fragment_loc = "./data/scripts/fragment.frag"
    self.vertex_loc = "./data/scripts/vertex.vert"
    self.noise_img1 = pygame.image.load('./data/images/misc/pnoise.png').convert_alpha()
    self.noise_img2 = pygame.image.load('./data/images/misc/pnoise2.png').convert_alpha()
    self.shader_obj = pg.Shader(True, self.vertex_loc, self.fragment_loc)

    flower_objs = self.tilemap.get_objs('flower')
    self.flower = pg.entities.Flowers(flower_objs, self.assets, self)
    self.gust = pg.entities.Gust(self)

    self.citizens = []
    self.water_pos = []
    self.fire_pos = []
    self.enemy_locs = []
    self.flows = []
    self.machines = []
    self.ghost = []
    self.ghost_locs = []
    self.fireballs = []
    self.dimension_loc = []
    self.end_rects = []
    self.heart_rects = []
    self.cage_brother_rects = []

    self.sparks = []

    for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1), ('spawners', 2), ('spawners', 3), ('spawners', 4), ('spawners', 5), ('spawners', 6), ('spawners', 7) ,('spawners', 8), ('spawners', 9), ('spawners', 10), ('spawners', 11)]):
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
        self.ghost_locs.append(spawner['pos'])
      elif spawner['variant'] == 7:
        self.dimension_loc.append(spawner['pos'])
      elif spawner['variant'] == 8:
        self.fireballs.append(pg.entities.Fireball(self, spawner['pos'], [1024 * 0.1, 1024 * 0.1 ] ,move_speed=5, cooldown=10))
      elif spawner['variant'] == 9:
        self.heart_rects.append(pygame.rect.Rect(spawner['pos'][0], spawner['pos'][1], 16,16))
      elif spawner['variant'] == 10:
        self.end_rects.append(pygame.rect.Rect(spawner['pos'][0], spawner['pos'][1], 16, 16))
      elif spawner['variant'] == 11:
        self.cage_brother_rects.append(pygame.rect.Rect(spawner['pos'][0], spawner['pos'][1], 32, 45))
    
    for fire_pos in self.tilemap.extract([('decor', 4),], True):
      self.fire_pos.append(fire_pos)

    #set the dimension
    if len(self.dimension_loc) == 2:
      self.min_dimension = [min(self.dimension_loc[0][0], self.dimension_loc[1][0]) // 16 + 2, min(self.dimension_loc[0][1], self.dimension_loc[1][1]) // 16 + 1]
      self.max_dimension = [max(self.dimension_loc[0][0], self.dimension_loc[1][0]) // 16 - 1, (max(self.dimension_loc[0][1], self.dimension_loc[1][1]) // 16) ]

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

    for loc in self.ghost_locs:
      self.ghost.append(pg.entities.Ghost(self, loc, (self.assets['ghost'].get_width(), self.assets['ghost'].get_height()), self.enemy ))

    self.true_scroll = [0,0]
    self.full_screen = False
    self.fire_particles = []
    for obj in self.fire_pos:
      self.fire_particles.append(pg.ui.Flame((obj['pos'][0] + 10, obj['pos'][1] + 2)))
    # self.scroll = [0,0]
    self.settings_window = False
    self.darkness = 0

    self.dead = -10
    self.transition = -30

    self.polysparks = []
    self.in_flow = False

    if level is None:
      self.world_completed = True #Needs to be false
    else:
      self.world_completed = False
    self.typing = False

    self.cage_bro_health = 100
    self.cage_ani = self.assets['cage'].copy()
    self.end_scene_time = 0

    self.game_over = False

    self.updated_record_timer = False
    self.tmin = 0
    self.tsec = 0
    self.img = None

    self.ghost_creation_last_update = 0
    self.ghost_creation_cooldown = 20000
    # self.fireball = pg.entities.Fireball(self, (295,154))

  @pg.pygs
  def run(self):
      self.clock.tick(60)
      if self.dead > 0:
        if self.dead == 1:
          self.sfx['death'].play()
        self.dead += 1
        if self.dead >= 50:
          self.transition = min(self.transition + 1, 30)
        if self.dead > 80:
          self.load_level(self.world[self.curr_world])

      '''
      REMEMBER TO UNCOMMENT THE BELOW SET OF CODE
      '''

      # if self.player.who == "h":
      #   if len(self.enemy.enemies) == 0 and len(self.ghost) == 0:
      #     self.transition += 1

      for end_rect in self.end_rects:
        if end_rect.colliderect(self.player.rect()):
          self.transition += 1
      

      if self.transition > 30:
        print("In the transition")
        self.curr_level += 1
        self.dead = -10
        if self.curr_level > self.world[self.curr_world][0]:
          #world is completed
          print("world is completed")
          self.world_completed = True
          self.load_level(level=None, text=self.world[self.curr_world][1])
          # self.curr_level = 1
          # self.curr_world += 1
        else:
          self.load_level(self.world[self.curr_world])
        
      time = pygame.time.get_ticks()
      # print(self.player.rect()[0], self.player.rect()[1])
      # print(self.clock.get_fps())
      self.ui_display.fill((0,0,0,0))
      self.display.fill((2,2,2))


      if self.player.who == "j":
        if self.curr_world > 2 and self.curr_level == 2:
          self.player.update_who("h")
        elif self.curr_world > 0  and self.tmin > 0:
          self.player.update_who("h")
      else:
        if time - self.ghost_creation_last_update > self.ghost_creation_cooldown:
          self.ghost.append(pg.entities.Ghost(self, [self.player.rect().x + random.random() * self.display.get_width(), self.player.rect().y + random.random() * self.display.get_height()], (self.assets['ghost'].get_width(), self.assets['ghost'].get_height()), self.enemy ))
          self.ghost_creation_last_update = time
      
      if self.cage_bro_health <= 0:
        self.ghost = []


      if not self.updated_record_timer:
        self.tmin, self.tsec = pg.convert_to_min_sec((time - self.start_time) // 1000)
        self.img = self.font.render(str(self.tmin) + " : " + str(self.tsec), True, (255,255,255))
      if self.curr_world != 0:
        self.ui_display.blit(self.img, (20,20))

      if self.transition < 0:
        self.transition += 1

      self.screenshake = max(0, self.screenshake - 1)

      controls = self.hud.get_controls()
      if self.dead <= 0 :
        self.movement = [False, False]
        if not self.settings_window:
          if controls['left'] :
            self.movement[0] = True
          if controls['right']:
            self.movement[1] = True
      
      #heart
      if self.dead <= 0 and not self.world_completed:
        for x in range(abs(self.dead) + 1):
          self.ui_display.blit(self.assets['heart'], (600 - x * 20, 20))

      self.true_scroll[0] += (self.player.rect().x - self.true_scroll[0] - 1280//4) / 5
      self.true_scroll[1] += (self.player.rect().y - self.true_scroll[1] - 720//4) / 20

      self.true_scroll[0] = max(self.min_dimension[0]*self.tilemap.tile_size, min( self.max_dimension[0] * self.tilemap.tile_size - self.display.get_width(), self.true_scroll[0] ))
      self.true_scroll[1] = max(self.min_dimension[1]* self.tilemap.tile_size, min(self.max_dimension[1] * self.tilemap.tile_size - self.display.get_height(), self.true_scroll[1] ))

      self.scroll = self.true_scroll.copy()
      self.scroll[0] = int(self.scroll[0])
      self.scroll[1] = int(self.scroll[1])

      self.tilemap.render(self.display, self.scroll)

      self.flower.update(self.player.rect(), self.display, self.scroll, time, self.gust.wind())

      for citizen in self.citizens:
        citizen.update(self.tilemap, (0,0), self.dt, (self.player.rect().centerx, self.player.rect().centery))
        citizen.render(self.display, offset=self.scroll)
      
      for machine in self.machines:
        machine.update(0.01)
        machine.render(self.display, self.scroll)
      
      for ghost in self.ghost.copy():
        if ghost.alive:
          ghost.update((self.player.rect().x, self.player.rect().y))
          ghost.render(self.display, self.scroll)
        else:
          self.ghost.remove(ghost)
      
      for arrow in self.arrows.copy():
        if not arrow.alive:
          self.arrows.remove(arrow)
        else:
          arrow.update(self.tilemap, (0,0), self.dt, self.gust.wind())
          arrow.render(self.display, self.scroll)
          if arrow.rect().colliderect(self.player.rect()) and abs(self.player.dashing[1]) < 1 and abs(self.player.dashing[0]) < 1 and not self.in_flow:
            arrow.alive = False
            self.dead += 1
            self.screenshake = max(16, self.screenshake)
            for x in range(30):
              angle = random.random() * math.pi * 2
              speed = random.random() * 5
              self.sparks.append(pg.ui.Spark(self.player.rect().center, angle, 2 + random.random()))
              self.particles.append(pg.ui.Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5 ], frame=random.randint(0,7)))
      
      self.enemy.update(self.tilemap, self.display, self.scroll, self.dt)

      self.in_flow = False
      for flow in self.flows.copy():
        flow.render(self.display, self.scroll)
        if flow.rect.colliderect(self.player.rect()):
          self.in_flow = True
          self.player.pos[0] = flow.rect.center[0] - 9
          self.player.pos[1] = flow.rect.center[1] - 9
          #give them an extra dash if they don't have one
          self.player.dashes = 1
          self.player.velocity[1] = 0
          #if player hits remove flow
          if self.player.hit:
            self.flows.remove(flow)
        if time - flow.last_shoot > self.flow_shoot_cooldown and pg.distance_between(flow.pos, (self.player.rect()[0], self.player.rect()[1])) <= 350 and not self.in_flow:
          flow.shoot()
          flow.last_shoot = time

      if not self.game_over:
        if not self.typing:
          self.player.update(self.tilemap, [self.movement[1] - self.movement[0], 0], self.dt, self.gust.wind())
        self.player.render(self.display, self.scroll)
      self.display.blit(self.pglow_img, (self.player.rect().center[0] - 255 //2 - self.scroll[0] , self.player.rect().center[1] - 255//2 - self.scroll[1] ), special_flags=BLEND_RGBA_ADD)
      
      for fireball in self.fireballs:
        fireball.update(time)
        fireball.render(self.display, self.scroll)
        if fireball.rect.colliderect(self.player.rect()) and abs(self.player.dashing[0]) < 2 and abs(self.player.dashing[1]) < 2:
          self.screenshake = max(16, self.screenshake)
          if time - fireball.last_attack_update > fireball.thingy_cooldown:
            self.dead += 1
            fireball.last_attack_update = time
            for x in range(30):
              angle = random.random() * math.pi * 2
              speed = random.random() * 5
              self.sparks.append(pg.ui.Spark(self.player.rect().center, angle, 2 + random.random(), (236,123,0)))
              self.polysparks.append(pg.ui.PolySpark([self.player.rect().centerx - self.scroll[0] ,self.player.rect().centery - self.scroll[1]], math.radians(random.randint(0,360)), random.randint(2,3), (255,random.randint(100,123),0), 2, 2))

      for particle in self.fire_particles:
        particle.draw_flame(self.display, self.scroll)
      


      if self.settings_window:
        self.settings.render(self.ui_display, time)
      
      #lamp img 
      for lamp in self.lamp_positions:
        pos = lamp['pos']
        self.display.blit(self.lamp_img, (pos[0] - self.scroll[0] - 24, pos[1] - self.scroll[1] + 30), special_flags=BLEND_RGBA_ADD)
        self.display.blit(self.lamp_glow_img, (pos[0] - self.scroll[0] - 17, pos[1] - self.scroll[1] - 10), special_flags=BLEND_RGBA_ADD)

      self.gust.update(time)
      
      for rect in self.cage_brother_rects:
        if self.cage_bro_health > 0:
          self.display.blit(self.cage_ani.img(), (rect[0] - self.scroll[0], rect[1] - self.scroll[1]))
          if self.player.hit and self.player.get_hit_rect().colliderect(rect):
            self.screenshake = max(self.screenshake, 24)
            self.cage_bro_health -= 0.5
            for x in range(5):
              angle = random.random() * math.pi * 2
              self.sparks.append(pg.ui.Spark(self.player.get_hit_rect().center, angle, 2 + random.random() * 5, (155,178,179)))
          if self.cage_bro_health > 70:
            self.cage_ani.frame = 0
          elif self.cage_bro_health > 40:
            self.cage_ani.frame = 1
          else:
            self.cage_ani.frame = 2
      
      if not self.game_over:
        for rect in self.heart_rects.copy():
          self.display.blit(self.assets['heart'], (rect[0] - self.scroll[0], rect[1] - self.scroll[1]))
          if self.dead <= 0 and rect.colliderect(self.player.rect()):
            self.dead = max(self.dead - 1, self.max_hearts)
            self.heart_rects.remove(rect)
            self.sfx['pickup'].play()
            for x in range(20):
              self.polysparks.append(pg.ui.PolySpark([self.player.rect().centerx - self.scroll[0] ,self.player.rect().centery - self.scroll[1]], math.radians(random.randint(0,360)), random.randint(2,3), (255,61,137), 2, 2))

      self.fireflies.recursive_call(time, self.display, self.scroll, self.dt)
      self.leaf.recursive_call(time, self.display, self.scroll, self.gust.wind(), dt=self.dt)

      if self.world_completed and self.player.rect().colliderect(self.home_rect):
        if not self.done_typing:
          self.typing = True
          pygame.draw.rect(self.ui_display, (0,0,0), pygame.rect.Rect(0,0, 640, 180))
          if self.curr_world != 0:
            if not self.updated_record_timer:
              if self.settings.record_time[str(self.curr_world)] == 0:
                self.settings.record_time[str(self.curr_world)] = (time - self.start_time) // 1000
              elif self.settings.record_time[str(self.curr_world)] - ((time - self.start_time) // 1000) > 0:
                self.settings.record_time[str(self.curr_world)] = (time - self.start_time) // 1000
              self.updated_record_timer = True
            rtmin, rtsec = pg.convert_to_min_sec(self.settings.record_time[str(self.curr_world)])
            rimg = self.font.render(str(rtmin) + " : " + str(rtsec), True, (255,255,255))
            self.ui_display.blit(rimg, (350,20))
            self.ui_display.blit(self.img, (300,20))
          self.done_typing = self.typer.update(time, self.ui_display, enter_loc=(550,100))
          if self.typer.banana_turn % 2 != 0:
            self.ui_display.blit(self.player_talk.img(), (10,10))
            self.player_talk.update()
          else:
            self.ui_display.blit(self.citizen_talk.img(), (10,10))
            self.citizen_talk.update()
        else:
          self.typing = False
          self.done_typing = False
          #done typing so update the world state 
          #check for game over
          self.curr_world += 1
          self.curr_level = 1
          #update the timer
          self.start_time = pygame.time.get_ticks()
          self.world_completed = False
          self.load_level(self.world[self.curr_world])
      else:
        self.typing = False
      
      if self.game_over:
        if not self.game_over_typing:
          pygame.draw.rect(self.ui_display, (0,0,0), pygame.rect.Rect(0,0, 640, 180))
          self.game_over_typing = self.game_over_typer.update(time, self.ui_display, enter_loc=(550,100))
          self.ui_display.blit(self.citizen_talk.img(), (10,10))
          self.citizen_talk.update()
      
      if self.cage_bro_health <= 0:
        self.sparks = []
        self.end_scene_time += 1
        if self.end_scene_time < 350:
          pygame.draw.rect(self.display, (0,0,0), (0,0,self.display.get_width(), self.display.get_height()))
        else:
          self.game_over = True
          self.display.blit(self.assets['bro'], (self.cage_brother_rects[0].x - self.scroll[0], self.cage_brother_rects[0].y + 22 - self.scroll[1]))
        #game over screen. 
        colors = [(255,255,255), (255,0,0)]
        if self.end_scene_time < 250:
          for x in range(10):
            angle = random.random() * math.pi * 2
            speed = random.random() * 5
            self.sparks.append(pg.ui.Spark(self.player.rect().center, angle, 2 + random.random() * speed, colors[random.randint(0,1)]))
        elif self.end_scene_time < 300:
          self.display.blit(self.assets['flash'].img(), (-350,-270))
          self.assets['flash'].update()
      
      for spark in self.sparks.copy():
        kill = spark.update()
        spark.render(self.display, self.scroll, self.dt)
        if kill:
          self.sparks.remove(spark)

      if self.curr_world == 0:
        if self.story_cooldown:
          pygame.draw.rect(self.ui_display, (0,0,0), (0,0,self.display.get_width(), self.display.get_height()))
          self.ui_display.blit(self.assets['story'], (7,25))
          self.story_cooldown = max(0, self.story_cooldown - 1)

      self.hud.events(self.settings.controls_keyboard)
      

Game().run()
