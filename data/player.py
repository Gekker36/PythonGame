import pygame as pg
from data import setup
from . import main as m
from . import tools as t
import math
import time


class Player(pg.sprite.Sprite):
    def __init__(self, location, world, direction=pg.K_RIGHT):
        pg.sprite.Sprite.__init__(self)
        self.image = setup.CFX['Character'].convert()
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(topleft = location)
        self.world = world
        self.true_pos = list(self.rect.center)
        
        self.spritesheet = self.create_spritesheet_dict()
        self.animationsheet = self.create_animation_dict()
        
        self.remainder = [0, 0]  #Adjust rect in integers; save remainders.
        self.direction = direction
        self.direction_stack = []  #Held keys in the order they were pressed.
        self.state = 'Idle'
        
        self.inventory = m.Inventory()
        self.inventory.add_item(m.Consumable('Healthpotion'))
        self.inventory.add_item(m.Weapon('Sword'))
        self.healthCurrent = 100
        self.healthMax = 100
        self.healthRegen = 1
        self.manaCurrent = 50
        self.manaMax = 100
        self.manaRegen = 10
        self.movespeed = 500
        self.level = 1
        self.experience = 0
        self.action = False
        self.faith = 100
        
        
        self.equipped = {"Head":[], "Body":[], "Weapon":[], "Shield":[]}
        self.attack = 10
        self.defence = 10
        
    def gainExperience(self, experience):
        self.experience += experience
        
    def castFireball(self):
        print("Casting Fireball")
        # Spell(self)
        
    def craft(self, item):
        self.inventory.add_item(item)

            
    def add_direction(self, key):
        """Add a pressed direction key on the direction stack."""
        if key in t.DIRECT_DICT:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            self.direction_stack.append(key)
            self.direction = self.direction_stack[-1]

    def pop_direction(self, key):
        """Pop a released key from the direction stack."""
        if key in t.DIRECT_DICT:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            if self.direction_stack:
                self.direction = self.direction_stack[-1]
    
    def startAction(self):
        self.action = True
        
    def stopAction(self):
        self.action = False
        
        
    def update(self, obstacles, dt):
        """Adjust the image and move as needed."""
        vector = [0, 0]
        for key in self.direction_stack:
            vector[0] += t.DIRECT_DICT[key][0]
            vector[1] += t.DIRECT_DICT[key][1]
        factor = (t.ANGLE_UNIT_SPEED if all(vector) else 1)
        frame_speed = self.movespeed*factor*dt
        self.remainder[0] += vector[0]*frame_speed
        self.remainder[1] += vector[1]*frame_speed
        vector[0], self.remainder[0] = t.divfmod(self.remainder[0], 1)
        vector[1], self.remainder[1] = t.divfmod(self.remainder[1], 1)
        if vector != [0, 0]:
            self.movement(obstacles, vector[0], 0)
            self.movement(obstacles, vector[1], 1)
        self.true_pos = list(self.rect.center)
        self.true_pos[1] += 20
        
        playerTile = [s for s in self.world.tilemap if s.rect.collidepoint(self.true_pos)]
        self.currentTile = playerTile[0]
        
        action_pos=self.true_pos
        
        if self.direction == 273:       #UP
            action_pos[1] = self.true_pos[1]-64
        if self.direction == 275:       #Right
            action_pos[0] = self.true_pos[0]+64 
        if self.direction == 274:       #DOWN
            action_pos[1] = self.true_pos[1]+64 
        if self.direction == 276:       #LEFT
            action_pos[0] = self.true_pos[0]-64 
        
        actionTile = [s for s in self.world.tilemap if s.rect.collidepoint(action_pos)]
        self.actionTile = actionTile[0]
            
            
        hit=self.actionTile.rect.collidelist(self.world.resource_rect)
        
        if hit != -1 and self.action:
            target = self.world.resources[hit]
            target.add_work(dt)
            if target.jobTimer >= target.jobTime:
                loot = target.get_loot()
                for l in loot:
                    self.inventory.add_item(l)
                print(self.inventory.items)
        
        self.animation()
        
            
    def movement(self, obstacles, offset, i):
        """Move player and then check for collisions; adjust as necessary."""
        self.rect[i] += offset
        collisions = pg.sprite.spritecollide(self, obstacles, False)
        callback = pg.sprite.collide_mask
        while pg.sprite.spritecollideany(self, collisions, callback):
            self.rect[i] += (1 if offset<0 else -1)
            self.remainder[i] = 0
            
    def create_spritesheet_dict(self):
        spritesheet = {}
        image_list = []
        for sprite in setup.CFX:
            spritesheet[sprite] = setup.CFX[sprite]
        return spritesheet
        
    def create_animation_dict(self):
        image_dict = self.spritesheet
        up_walk_list    = [image_dict['up_stand'], image_dict['up_walk1'], image_dict['up_walk2']]
        down_walk_list  = [image_dict['down_stand'], image_dict['down_walk1'], image_dict['down_walk2']]
        right_walk_list = [image_dict['right_stand'], image_dict['right_walk1'], image_dict['right_walk2']]
        left_walk_list  = [image_dict['left_stand'], image_dict['left_walk1'], image_dict['left_walk2']]
        
        direction_dict= {  'left': left_walk_list,
                                'right': right_walk_list,
                                'up': up_walk_list,
                                'down': down_walk_list}
                                
        return direction_dict
            
    def animation(self):
        if self.direction == 273:         #UP
            self.image = self.animationsheet['up'][0]
        elif self.direction == 274:       #DOWN
            self.image = self.animationsheet['down'][0]
        elif self.direction == 275:       #Right
            self.image = self.animationsheet['right'][0]
        elif self.direction == 276:       #LEFT
            self.image = self.animationsheet['left'][0] 
        
                
    def draw(self, surface):
        surface.blit(self.image, self.rect)