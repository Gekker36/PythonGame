from data.states import  level #, death, shop, levels, battle,
# from data.states import credits
from . import setup, tools, inputcontroller, GUI
from . import constants as c
from . import NPCstates
import pygame as pg
import random
import math
import time







ANGLE_UNIT_SPEED = math.sqrt(2)/2
DIRECT_DICT = {pg.K_LEFT  : (-1, 0),
               pg.K_RIGHT : ( 1, 0),
               pg.K_UP    : ( 0,-1),
               pg.K_DOWN  : ( 0, 1)}
               
itemlist = {
        'sword': {
                'icon': 'DARKGREEN',
                'value': 100,
                'stats':{'attack':15},
                'weight': 1
                },
        'shield': {
                'icon': 'BROWN',
                'value': 50,
                'stats':{'defence':10},
                'weight': 1
                }, 
        'healthpotion': {
                'icon': 'YELLOW',
                'value' : 10,
                'stats':{'currentHealth':10},
                'weight': 2
                }
        }
               

class Player(pg.sprite.Sprite):
    def __init__(self, location, world, direction=pg.K_RIGHT):
        pg.sprite.Sprite.__init__(self)
        self.image = setup.CFX['Character']#.convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(topleft = location)
        self.world = world
        self.true_pos = list(self.rect.center)
        
       
        
        self.remainder = [0, 0]  #Adjust rect in integers; save remainders.
        self.direction = direction
        self.old_direction = None  #The Players previous direction every frame.
        self.direction_stack = []  #Held keys in the order they were pressed.=
        
        
        self.inventory = Inventory()
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

            
    def add_direction(self, key):
        """Add a pressed direction key on the direction stack."""
        if key in DIRECT_DICT:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            self.direction_stack.append(key)
            self.direction = self.direction_stack[-1]

    def pop_direction(self, key):
        """Pop a released key from the direction stack."""
        if key in DIRECT_DICT:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            if self.direction_stack:
                self.direction = self.direction_stack[-1]
    

    def update(self, obstacles, dt):
        """Adjust the image and move as needed."""
        vector = [0, 0]
        for key in self.direction_stack:
            vector[0] += DIRECT_DICT[key][0]
            vector[1] += DIRECT_DICT[key][1]
        factor = (ANGLE_UNIT_SPEED if all(vector) else 1)
        frame_speed = self.movespeed*factor*dt
        self.remainder[0] += vector[0]*frame_speed
        self.remainder[1] += vector[1]*frame_speed
        vector[0], self.remainder[0] = divfmod(self.remainder[0], 1)
        vector[1], self.remainder[1] = divfmod(self.remainder[1], 1)
        if vector != [0, 0]:
            self.movement(obstacles, vector[0], 0)
            self.movement(obstacles, vector[1], 1)
        self.true_pos = list(self.rect.center)
        
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
                # self.world.jobQueue.remove_job(target)
                self.inventory.add_item(Item())
                print(self.inventory.items)
        

        
        
            
    def movement(self, obstacles, offset, i):
        """Move player and then check for collisions; adjust as necessary."""
        self.rect[i] += offset
        collisions = pg.sprite.spritecollide(self, obstacles, False)
        callback = pg.sprite.collide_mask
        while pg.sprite.spritecollideany(self, collisions, callback):
            self.rect[i] += (1 if offset<0 else -1)
            self.remainder[i] = 0
            
                
    def draw(self, surface):
        surface.blit(self.image, self.rect)


        
class Enemy(pg.sprite.Sprite):
    def __init__(self, location, world):
        pg.sprite.Sprite.__init__(self)
        self.image = setup.GFX['Enemy'].convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = location[0]
        self.rect.y = location[1]
        
        self.sight_range = 500
        self.sight_rect = pg.Rect(-self.sight_range/2+self.rect.x,
                                -self.sight_range/2+self.rect.y, 
                                self.sight_range, 
                                self.sight_range)
        
        self.true_pos = list(self.rect.center)
        self.remainder = [0, 0]  #Adjust rect in integers; save remainders.
        self.FSM = NPCstates.FSM(self)
        self.FSM.setState("Idle")
        
        self.inventory = Inventory()
        self.healthCurrent = 100
        self.healthMax = 100
        self.healthRegen = 1
        self.movespeed = 300 #random.randint(0,200)
        self.world = world
        self.target = None

    def set_target(self, target):
        self.target = target
        
    def update(self, obstacles, dt):
        if self.healthCurrent <= 0:
            self.kill()
        
        if not self.target and self.world.jobQueue.jobs:
            job = self.world.jobQueue.jobs[0]
            self.target = job
            self.world.jobQueue.remove_job(job)
            
        if self.target:
            
            posDif = [self.target.rect.x-self.rect.x, self.target.rect.y-self.rect.y]
            if not self.rect == self.target:    
                vector = [0, 0]
                dist = min(self.movespeed*dt, math.sqrt((posDif[0]**2)+(posDif[1]**2)))
                totAngle = abs(posDif[0])+abs(posDif[1])
                vector = [dist*posDif[0]/totAngle,dist*posDif[1]/totAngle]

                if vector != [0, 0]:
                    self.rect[0] += vector[0]
                    self.rect[1] += vector[1]
            
            
            if sum(posDif) <= 10:
                # print('At target')
                self.target.add_work(dt)
                if self.target.jobTimer >= self.target.jobTime:
                    self.target = None
                    self.inventory.add_item(Item())
                    print(len(self.inventory.items))
                
        # self.true_pos = list(self.rect.center)          
        # hit = pg.sprite.spritecollide(self, resource_sprites, False)
        # 
        # if hit and hit[0] == self.target:
        #     hit[0].add_work(dt)
        #     if hit[0].jobTimer >= hit[0].jobTime:
                
        
        

                
        for character in self.world.characters:
            dist = math.sqrt((character.true_pos[0] - self.true_pos[0])**2 + (character.true_pos[1] - self.true_pos[1])**2)


        self.FSM.execute()
                
    def movement(self, obstacles, offset, i):
        """Move player and then check for collisions; adjust as necessary."""
        self.rect[i] += offset
        collisions = pg.sprite.spritecollide(self, obstacles, False)
        callback = pg.sprite.collide_mask
        while pg.sprite.spritecollideany(self, collisions, callback):
            self.rect[i] += (1 if offset<0 else -1)
            self.remainder[i] = 0
        
    def draw(self, surface):
        pg.draw.rect(surface, c.blue, self.sight_rect)
        surface.blit(self.image, self.rect) 
        
class Spell(pg.sprite.Sprite):
    def __init__(self, player):
        self.manaCost = 10
        if player.manaCurrent >= self.manaCost:
            pg.sprite.Sprite.__init__(self, player.world.spell_sprites)
            self.image = setup.GFX['Orb of Flame'].convert()
            self.rect = self.image.get_rect()
            self.rect.x = player.rect.x
            self.rect.y = player.rect.y
            self.image.set_colorkey((0,0,0))
            self.direction = player.direction
            self.speed = 4
            self.caster = player
            # player.manaCurrent -= self.manaCost
            
    def update(self, deltatime):
        
        if self.direction == 273:
            self.rect.y -= self.speed #UP
        if self.direction == 275:
            self.rect.x += self.speed #Right
        if self.direction == 274:
            self.rect.y += self.speed #DOWN
        if self.direction == 276:
            self.rect.x -= self.speed #LEFT
            
        hit = pg.sprite.spritecollide(self, character_sprites,False)
        
        if hit:
            if hit[0] != self.caster:
                hit[0].healthCurrent -= 25
                if hit[0].healthCurrent <=0:
                    self.caster.gainExperience(10)
                self.kill()
            
        if self.rect.x >= c.mapWidth*c.tileSize or self.rect.x <= -c.tileSize or self.rect.y >= c.mapHeight*c.tileSize or self.rect.y <= -c.tileSize:
            self.kill()
       
    def draw(self, surface):
        surface.blit(self.image, self.rect)  
        
class Chest(pg.sprite.Sprite):
    def __init__(self, currentTile):
        pg.sprite.Sprite.__init__(self)
        self.inventory = Inventory()
        self.inventory.add_item(Item())
        self.image = setup.GFX["Chest Closed"]
        self.rect = self.image.get_rect()
        self.rect.x = currentTile.rect.x
        self.rect.y = currentTile.rect.y
        self.isOpen = False
        
        
    def update(self):
        pass
        
    def draw (self, surface):
        surface.blit(self.image, self.rect)
    
class Item(object):
    def __init__(self):
        self.image = setup.GFX['Sword_icon']
        self.name = "Sword"
        self.type = "Weapon"
        self.isStackable = False
        self.price = 100
        self.amount = 1       
        
class Inventory(object):
    def __init__(self):
        self.size = 10
        self.items=[]

        
    def add_item(self, item):
        for i in self.items:
            if i.name == item.name and i.isStackable == True:
                i.amount +=1
                return
        
        if len(self.items)<self.size:
            self.items.append(item)
        else:
            print("Inventory is full")
            
    def remove_item(self, item):
        self.items.remove(item)
        
        
class Job(object):
    def __init__(self,job):
        self.job = job
        
    
class JobQueue(object):
    def __init__(self):
        self.jobs = []
        
    def add_job(self, job):
        self.jobs.append(job)
            
    def remove_job(self, job):
        self.jobs.remove(job)
        
          
class Block(pg.sprite.Sprite):
    """Something to run head-first into."""
    def __init__(self, location):
        """The location argument is where I will be located."""
        pg.sprite.Sprite.__init__(self)
        self.image = setup.GFX['stone_block'].convert()
        self.rect = self.image.get_rect(topleft = location)
        self.mask = pg.mask.from_surface(self.image)
        
class Resource(object):
    def __init__(self, currentTile):
        pg.sprite.Sprite.__init__(self)
        self.image = setup.GFX['Stone_Deposit'].convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.x = currentTile.rect.x
        self.rect.y = currentTile.rect.y
        self.jobTime = 2
        self.jobTimer = 0
        self.worked = False
    
    def add_work(self, dt):
        self.worked=True
        self.jobTimer +=dt

        
    def update(self, dt):
        if self.worked:
            self.worked = False
            if self.jobTimer>= self.jobTime:
                self.kill()
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
class Tile(object):
    def __init__(self,world,x,y,tileType):
        self.tileType = tileType
        self.image = setup.TMX[self.tileType].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x*64
        self.rect.y = y*64
        self.mask = pg.mask.from_surface(self.image)
        self.world = world
        self.isPassable = True
        self.hasCrop = False
        self.crop =[]

    def plant_crop(self, crop):
        # print("Planting crop")
        # self.crop= crop
        self.hasCrop = True
        self.croptTimer=0
        
    def harvest_crop(self):
        # self.crop=[]
        self.hasCrop = False
        
    def update(self, dt):
        self.image = setup.TMX[self.tileType]
        
        if self.hasCrop:
            self.cropTimer += dt
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

        
class World(object):
    def __init__(self,viewport):
        self.mapHeight = c.mapHeight
        self.mapWidth = c.mapWidth
        self.tileSize = c.tileSize
        self.worldGenerator()
        
        self.characters = []
        self.resources = []
        # self.chests = []
        
        # self.growable = []
        # self.growing = []
        # self.harvestable = []
        self.jobQueue = JobQueue()
        
        self.character_sprites = pg.sprite.Group()
        self.spell_sprites = pg.sprite.Group()
        self.resource_sprites = pg.sprite.Group()
        self.resource_rect = []
        self.object_sprites = pg.sprite.Group()
        
        self.player = (Player((400,400), self))
        self.character_sprites.add(self.player)
        self.characters.append(self.player)
    
    def worldGenerator(self):
        print("Create tilemap")
        
        self.tilemap=[]
        self.tilemap_rect=[]
        
        for h in range(self.mapHeight):
            for w in range(self.mapWidth):
                tile = Tile(self,w,h,'Grass')
                self.tilemap.append(tile)
                self.tilemap_rect.append(tile.rect)
        
        obstacles = [Block((64*w,0)) for w in range(self.mapWidth)]
        obstacles.append([Block((64*w,(self.mapHeight-1)*self.tileSize)) for w in range(self.mapWidth)])
        obstacles.append([Block((0,64*h)) for h in range(self.mapHeight)])
        obstacles.append([Block(((self.mapWidth-1)*self.tileSize,64*h)) for h in range(self.mapHeight)])
        self.obstacles = pg.sprite.Group(obstacles)
        
    def generate_resource(self,location):
        resource = Resource(location)
       
        # self.resource_sprites.add(resource)
        self.resources.append(resource)
        self.resource_rect.append(resource.rect)
        # self.obstacles.add(resource)
        # job = Job(resource)
        self.jobQueue.add_job(resource)
        # print(self.jobQueue.jobs)
    
    def create_chest(self, location):
        chest = Chest(location)
        self.object_sprites.add(chest)

    def change_tileType(self, tile, newTileType):
        tile.tileType = newTileType
        tile.image = setup.TMX[tile.tileType].convert_alpha()  
        if tile.tileType == 'Dirt':
            self.growable.append(tile)
            self.jobQueue.add_job(tile)
            
    def create_NPC(self, location):
        NPC = Enemy(location, self)
        self.character_sprites.add(NPC)

   ##   
    # def grow_crop(self, tile):
    #     self.growable.removable(tile)
    #     self.growing.append(tile)
    #     
    # def grown_crop(self, tile):
    #     self.growing.removable(tile)
    #     self.harvestable.append(tile)
    # 
    # def harvest_crop(self, tile):
    #     self.harvestable.removable(tile)
    #     self.growable.append(tile)
        
    
    def update(dt):
        for character in self.characters:
            character.update(self.obstacles, dt)

        
    def draw(self, surface, viewport):
        
        
        for tile in self.tilemap:
            if viewport.colliderect(tile.rect):
                tile.draw(surface)
                
                
        for character in self.characters:
            character.draw(surface)
        
        for resource in self.resources:
            resource.draw(surface)
        
        

            


class Control(object):
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.done = False
        self.keys=pg.key.get_pressed()
        self.logictimer = 0
        self.drawtimer = 0
        self.viewport = self.screen.get_rect()
        self.GUI = GUI.GUI(self.viewport, self)
        self.level = pg.Surface((c.mapWidth*c.tileSize,c.mapHeight*c.tileSize)).convert()
        self.level_rect = self.level.get_rect()

        
    def event_loop(self):
        inputcontroller.playerInput(self)

                
    def update(self,deltatime):
        t = time.time()
        
        self.world.spell_sprites.update(deltatime)
        self.world.resource_sprites.update(deltatime)
        self.world.character_sprites.update(self.world.obstacles, deltatime)
        self.update_viewport()
        self.GUI.update()
        
        
        
        self.logictimer +=deltatime
        if self.logictimer>1:
            # print(str('logictimer: ') + str(time.time()-t))
            self.logictimer=0
        
    def update_viewport(self):
        self.viewport.center = self.world.player.rect.center
        self.viewport.clamp_ip(self.level_rect)

                    
    def draw(self, deltatime):
        t = time.time()
        self.world.draw(self.level, self.viewport)
        self.world.obstacles.draw(self.level)
        self.world.spell_sprites.draw(self.level)
        self.world.resource_sprites.draw(self.level)
        self.world.object_sprites.draw(self.level)
        self.world.character_sprites.draw(self.level)
        self.GUI.draw(self.level,self.viewport)
        self.screen.blit(self.level, (0,0), self.viewport)

        pg.display.update()
        

        # self.drawtimer +=deltatime
        # if self.drawtimer>1:
        #     print(str('drawtimer: ') + str(time.time()-t))
        #     self.drawtimer=0
        
    def display_fps(self):
        """Show the program's FPS in the window handle."""
        caption = "{} - FPS: {:.2f}".format("Test Pygame", int(self.clock.get_fps()))
        pg.display.set_caption(caption)
  
    def main(self):

        print("Create world")
        self.world = World(self.screen_rect.copy())


        print("Starting main loop")
        while not self.done:
            self.deltatime = self.clock.tick()/1000
            self.event_loop()
            self.update(self.deltatime)
            self.draw(self.deltatime)
            pg.display.update()
            self.display_fps()
        
        
def divfmod(x, y):
    """Identical to the builtin divmod but using math.fmod to retain signs."""
    fmod = math.fmod(x, y)
    div = (x-fmod)//y
    return div, fmod
    
        
def main():
    print("Create GameControl")
    gameControl = Control().main()
    

    
   
    
    
    