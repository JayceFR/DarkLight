import pygame, math, random
from pygs.ui.particle import Particle
from pygs.ui.spark import Spark

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size, gravity=True):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.action = ''
        self.anim_offset = (0,0)
        self.flip = False
        self.last_movement = [0,0]
        self.momentum = [0,0]
        self.mass = 1
        self.speed = [1,1]
        self.current_speed = 0
        if gravity:
            self.set_action('idle')

    def __getitem__(self, item):
        return self.pos[item]
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/'+ self.action].copy()
        
    def update(self, tilemap, movement=(0, 0), dt = 1, gravity=True):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        frame_movement = (movement[0] + self.velocity[0] + self.momentum[0] / self.mass, movement[1] + self.velocity[1] + self.momentum[1] / self.mass)
        self.pos[0] += frame_movement[0] * self.speed[0] * dt
        entity_rect = self.rect()
        prects, type_of_rect = tilemap.physics_around(self.pos)
        for pos, rect in enumerate(prects):
            if entity_rect.colliderect(rect):
                if self.type == "player" and type_of_rect[pos] == "spike" and not self.game.dead:
                    #player is dead
                    self.game.dead = 1
                    for x in range(40):
                        angle = random.random() * math.pi * 2
                        speed = random.random() * 5
                        self.game.sparks.append(Spark(self.game.player.rect().center, angle, 2 + random.random()))
                        self.game.particles.append(Particle(self.game, 'particle', self.game.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5 ], frame=random.randint(0,7)))
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        
        self.pos[1] += frame_movement[1] * self.speed[1] * dt
        entity_rect = self.rect()
        prects, type_of_rect = tilemap.physics_around(self.pos)
        for pos, rect in enumerate(prects):
            if entity_rect.colliderect(rect):
                if self.type == "player" and type_of_rect[pos] == "spike" and not self.game.dead:
                    #player is dead
                    self.game.dead = 1
                    for x in range(30):
                        angle = random.random() * math.pi * 2
                        speed = random.random() * 5
                        self.game.sparks.append(Spark(self.game.player.rect().center, angle, 2 + random.random()))
                        self.game.particles.append(Particle(self.game, 'particle', self.game.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5 ], frame=random.randint(0,7)))
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.last_movement = movement
        
        if gravity:
            self.velocity[1] = min(7, self.velocity[1] + 0.2)

        
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        
        if gravity:
            self.animation.update()
        
    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        # pygame.draw.rect(surf, (255,0,0), (self.rect()[0] - offset[0], self.rect()[1] - offset[1], self.rect()[2], self.rect()[3]))
        # surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))

        