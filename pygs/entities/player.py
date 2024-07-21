import pygame, random, math
from .entity import PhysicsEntity
from ..ui.particle import Particle

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 2
        self.dashes = 1
        self.wall_slide = 0
        self.dashing = [0,0]
        self.max_speed = [5, 5] #left and right along x axis
        self.orig_max_speed = [5, 5]
        self.speed = [3,2.5] #just a scalar factor
        self.orig_speed = [3,2.5]
        self.last_time = 0
        self.time_update = 0
        self.acceleration = 0.05
        self.hit = 0  # amount, left, right, top, bottom
        self.hit_facing_right = True
        self.hit_facing_up = None
        self.hit_timer = 40
        self.hit_rect = (0,0,0,0)
        self.jump_buffer = 10
        self.can_wallslide = True
    
    def update(self, tilemap, movement = [0,0], dt = 1, wind = 0):
        if movement[0] > self.last_movement[0]:
            if wind in {-2, 0, 2}:
                self.max_speed[0] = self.orig_max_speed[0]
            self.velocity[0] -= 0.4
            self.speed[0] = self.orig_speed[0]
        if movement[0] < self.last_movement[0]:
            if wind in {-2, 0, 2}:
                self.max_speed[1] = self.orig_max_speed[1]
            self.velocity[0] += 0.4
            self.speed[0] = self.orig_speed[0]
        #acceleration
        if movement[0] > 0:
            self.speed[0] = min(self.speed[0] + self.acceleration, self.max_speed[1])
        if movement[0] < 0:
            self.speed[0] = min(self.speed[0] + self.acceleration, self.max_speed[0])

        # self.velocity[0] += wind * 0.01       
        super().update(tilemap, movement=movement, dt=dt)
        self.air_time += 1

        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 2
            self.dashes = 1
            self.can_wallslide = True
            if self.jump_buffer:
                self.jump()

        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4 and self.wall_slide == 0 and self.can_wallslide :
            self.wall_slide = 90
            self.can_wallslide = False
            #extra jump in wall slide
            self.jumps = min(self.jumps + 1, 2)
            #restock dashes
            self.dashes = 1
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True
        
        if self.wall_slide < 20:
            if self.hit > 0:
                if self.hit_facing_right is not None:
                    self.set_action('hit')
                if self.hit_facing_up is not None:
                    if self.hit_facing_up:
                        self.set_action('hit_up')
                    else:
                        self.set_action('hit_down')
            elif self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')
        else:
            if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4:
                self.velocity[1] = min(self.velocity[1], 0)
            else:
                self.wall_slide = 0
            if self.game.hud.get_controls()["up"]:
                self.velocity[1] = -0.5
            self.set_action('climb')
        
        self.wall_slide = max(0, self.wall_slide - 1)


        if abs(self.dashing[0]) in {40, 30} or abs(self.dashing[1]) in {40,30}:
            for x in range(20):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                pvel = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvel, frame=random.randint(0,7)))
        if self.dashing[0]> 0:
            self.dashing[0] = max(0, self.dashing[0] - 1)
        if self.dashing[0] < 0:
            self.dashing[0] = min(0, self.dashing[0] + 1)
        if self.dashing[1]> 0:
            self.dashing[1] = max(0, self.dashing[1] - 1)
        if self.dashing[1] < 0:
            self.dashing[1] = min(0, self.dashing[1] + 1)
        if abs(self.dashing[0]) > 30:
            self.velocity[0] = abs(self.dashing[0]) / self.dashing[0] * 3
            if abs(self.dashing[0]) == 31:
                self.velocity[0] *= 0.5
            pvel = [abs(self.dashing[0])/ self.dashing[0] * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvel, frame=random.randint(0,7)))
        if abs(self.dashing[1]) > 30:
            self.velocity[1] = abs(self.dashing[1]) / self.dashing[1] * 3
            if abs(self.dashing[1]) == 31:
                self.velocity[1] *= 0.6
                # self.velocity[1] = 0.5
            pvel = [abs(self.dashing[1])/ self.dashing[1] * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvel, frame=random.randint(0,7)))
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)
        
        # if self.game.hud.get_controls()["down"]:
        #     self.velocity[1] += 0.1
        
        if self.dashing[1]:
            if self.velocity[1] > 0:
                self.velocity[1] = max(self.velocity[1] - 0.05, 0)
            else:
                self.velocity[1] = min(self.velocity[1] + 0.1, 0)
            
        
        self.hit = max(0, self.hit - 0.5)
        if self.hit:
            self.velocity[0] = 0
            self.velocity[1] = 0
        
        self.hit_timer = min(40, self.hit_timer + 1)
        
        self.jump_buffer = max(0, self.jump_buffer - 1)
    
    def render(self, surf, offset=(0,0)):
        if abs(self.dashing[0]) <= 30:
            super().render(surf, offset=offset)
            # if self.hit > 0:
            #     pygame.draw.rect(surf, (255,0,0), (self.hit_rect[0] - offset[0], self.hit_rect[1] - offset[1], self.hit_rect[2], self.hit_rect[3]))
    
    def jump(self):
        if self.wall_slide > 20:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 1.5
                self.velocity[1] = -3
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -1.5
                self.velocity[1] = -3
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
        elif self.jumps:
            self.velocity[1] = -2.5
            self.jumps = max(0, self.jumps -1)
            self.air_time = 5
    
    def attack(self):
        if self.hit_timer >= 40:
            self.hit_timer = 0 
            self.hit = 10
            self.hit_facing_up = None
            self.hit_facing_right = not self.flip
            if self.flip:
                self.hit_rect = (self.pos[0] - self.size[0] - 10, self.pos[1], self.size[0] + 20, self.size[1] )
            else:
                self.hit_rect = (self.pos[0] , self.pos[1] , self.size[0] + 20, self.size[1] )
            if self.game.hud.get_controls()["up"]:
                self.hit_facing_right = None
                self.hit_facing_up = True
                self.hit_rect =  (self.pos[0] , self.pos[1] - self.size[1], self.size[0] , self.size[1] + 5 )
            elif self.game.hud.get_controls()["down"]:
                self.hit_facing_right = None
                self.hit_facing_up = False
                self.hit_rect = (self.pos[0] , self.pos[1] + self.size[1] //2 , self.size[0] , self.size[1] + 5 )
    
    def get_hit_rect(self):
        return pygame.rect.Rect(self.hit_rect[0], self.hit_rect[1], self.hit_rect[2], self.hit_rect[3])
    
    def dash(self):
        if self.dashes:
            if not self.dashing[0]:
                if self.game.hud.get_controls()["left"]:
                    self.dashing[0] = -38
                    self.game.screenshake = max(20, self.game.screenshake)
                if self.game.hud.get_controls()["right"]:
                    self.dashing[0] = 38
                    self.game.screenshake = max(20, self.game.screenshake)
                if self.game.hud.get_controls()["up"]:
                    self.dashing[1] = -38
                    self.game.screenshake = max(20, self.game.screenshake)
                if self.game.hud.get_controls()["down"]:
                    print("dashing down")
                    self.dashing[1] = 38
                    self.game.screenshake = max(20, self.game.screenshake)
            self.dashes = max(0, self.dashes -1)
