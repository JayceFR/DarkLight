import pygame, math

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
        for rect in tilemap.physics_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        
        self.pos[1] += frame_movement[1] * self.speed[1] * dt
        entity_rect = self.rect()
        for rect in tilemap.physics_around(self.pos):
            if entity_rect.colliderect(rect):
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
        # surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))

        