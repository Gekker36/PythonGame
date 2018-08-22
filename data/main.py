from data.states import  level #, death, shop, levels, battle,
# from data.states import credits
from . import setup, tools, inputcontroller
from . import constants as c
import pygame as pg
import random
import math
import time



character_sprites = pg.sprite.Group()
resource_sprites = pg.sprite.Group()
spell_sprites = pg.sprite.Group()



ANGLE_UNIT_SPEED = math.sqrt(2)/2
DIRECT_DICT = {pg.K_LEFT  : (-1, 0),
               pg.K_RIGHT : ( 1, 0),
               pg.K_UP    : ( 0,-1),
               pg.K_DOWN  : ( 0, 1)}


class Player(pg.sprite.Sprite):
    def __init__(self, location, direction=pg.K_RIGHT):
        # pg.sprite.Sprite.__init__(self,character_sprites)
        self.image = setup.GFX['Character'].convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(topleft = location)

        self.true_pos = list(self.rect.center)
        self.remainder = [0, 0]  #Adjust rect in integers; save remainders.
        self.direction = direction
        self.old_direction = None  #The Players previous direction every frame.
        self.direction_stack = []  #Held keys in the order they were pressed.
        self.redraw = False  #Force redraw if needed.
        
        self.movespeed = 500
        # self.inventory = Inventory()
        self.healthCurrent = 100
        self.healthMax = 100
        self.healthRegen = 1
        self.manaCurrent = 50
        self.manaMax = 100
        self.manaRegen = 10
        
        self.level = 1
        self.experience = 0
        self.working = False
        
        
        self.equipped = {"Head":[], "Body":[], "Weapon":[], "Shield":[]}
        self.attack = 10
        self.defence = 10
        
    def gainExperience(self, experience):
        self.experience += experience
        
    def castFireball(self):
        print("Casting Fireball")
        Spell(self)
    # 
    # def createChest(self):
    #     print("Creating Chest")
    #     Chest(self)
    #   
    # def createItem(self):
    #     self.inventory.add_item(Item())
    #     
   
            
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
                
    def update(self, obstacles, deltatime):
        """Adjust the image and move as needed."""
        vector = [0, 0]
        for key in self.direction_stack:
            vector[0] += DIRECT_DICT[key][0]
            vector[1] += DIRECT_DICT[key][1]
        factor = (ANGLE_UNIT_SPEED if all(vector) else 1)
        frame_speed = self.movespeed*factor*deltatime
        self.remainder[0] += vector[0]*frame_speed
        self.remainder[1] += vector[1]*frame_speed
        vector[0], self.remainder[0] = divfmod(self.remainder[0], 1)
        vector[1], self.remainder[1] = divfmod(self.remainder[1], 1)
        if vector != [0, 0]:
            self.movement(obstacles, vector[0], 0)
            self.movement(obstacles, vector[1], 1)
            
        hit = pg.sprite.spritecollide(self, resource_sprites,False)
        
        if hit:
            if self.working:
                hit[0].worked=True
            else:
                hit[0].worked = False

        
        
            
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
    def __init__(self, location,player):
        pg.sprite.Sprite.__init__(self,character_sprites)
        self.image = setup.GFX['Enemy'].convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = location[0]
        self.rect.y = location[1]
        
        self.true_pos = list(self.rect.center)
        self.remainder = [0, 0]  #Adjust rect in integers; save remainders.

        self.old_direction = None  #The Players previous direction every frame.
        self.direction_stack = []  #Held keys in the order they were pressed.
        self.redraw = False  #Force redraw if needed.
        
        self.healthCurrent = 100
        self.healthMax = 100
        self.healthRegen = 1
        self.movespeed = random.randint(0,200)
        self.target = player

    def set_target(self, target):
        self.target = target
        
    def update(self, obstacles, dt):
        if self.healthCurrent <= 0:
            self.kill()
            
        if self.target:
            if not self.rect == self.target:    
                vector = [0, 0]
                if (self.rect.x-self.target.rect.x)>0:
                    vector[0] = -1
                if (self.rect.x-self.target.rect.x)<0:
                    vector[0] = 1
                if (self.rect.y-self.target.rect.y)>0:
                    vector[1] = -1
                if (self.rect.y-self.target.rect.y)<0:
                    vector[1] = 1
                factor = (ANGLE_UNIT_SPEED if all(vector) else 1)
                frame_speed = self.movespeed*factor*dt
                self.remainder[0] += vector[0]*frame_speed
                self.remainder[1] += vector[1]*frame_speed
                vector[0], self.remainder[0] = divfmod(self.remainder[0], 1)
                vector[1], self.remainder[1] = divfmod(self.remainder[1], 1)
                if vector != [0, 0]:
                    self.movement(obstacles, vector[0], 0)
                    self.movement(obstacles, vector[1], 1)
                
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
        
class Spell(pg.sprite.Sprite):
    def __init__(self, player):
        self.manaCost = 10
        if player.manaCurrent >= self.manaCost:
            pg.sprite.Sprite.__init__(self, spell_sprites)
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
        
          
class Block(pg.sprite.Sprite):
    """Something to run head-first into."""
    def __init__(self, location):
        """The location argument is where I will be located."""
        pg.sprite.Sprite.__init__(self)
        self.image = setup.GFX['stone_block'].convert()
        self.rect = self.image.get_rect(topleft = location)
        self.mask = pg.mask.from_surface(self.image)
        
class Resource(pg.sprite.Sprite):
    def __init__(self, location):
        pg.sprite.Sprite.__init__(self,resource_sprites)
        self.image = setup.GFX['Deposit'].convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.x = location[0]
        self.rect.y = location[1]
        self.jobTime = 2
        self.jobTimer = 0
        self.worked = False

        
    def update(self, dt):
        if self.worked:
            self.jobTimer += dt
            if self.jobTimer>= self.jobTime:
                self.kill()
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
class Tile(object):
    def __init__(self,x,y,tileType):
        self.tileType = tileType
        self.image = setup.TMX[tileType].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x*64
        self.rect.y = y*64
        self.mask = pg.mask.from_surface(self.image)
        
        self.isPassable = True
        self.hasCrop = False
        self.crop =[]

    def plant_crop(self, crop):
        print("Planting crop")
        self.crop= crop
        self.hasCrop = True
        
    def harvest_crop(self):
        self.crop=[]
        self.hasCrop = False
        
    def update(self):
        self.image = setup.TMX[self.tileType]
        pass
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

        
class World(object):
    def __init__(self,viewport):
        self.mapHeight = c.mapHeight
        self.mapWidth = c.mapWidth
        self.tileSize = c.tileSize
        self.worldGenerator()
        self.resources = []

    
    def worldGenerator(self):
        print("Create tilemap")
        
        self.tilemap=[]
        
        for h in range(self.mapHeight):
            for w in range(self.mapWidth):
                self.tilemap.append(Tile(w,h,'Grass'))
        
        obstacles = [Block((64*w,0)) for w in range(self.mapWidth)]
        obstacles.append([Block((64*w,(self.mapHeight-1)*self.tileSize)) for w in range(self.mapWidth)])
        obstacles.append([Block((0,64*h)) for h in range(self.mapHeight)])
        obstacles.append([Block(((self.mapWidth-1)*self.tileSize,64*h)) for h in range(self.mapHeight)])
        self.obstacles = pg.sprite.Group(obstacles)
        
    def generate_resource(self,location):
        self.resources.append(Resource(location))
    
    def update(dt):
        pass
        
    def draw(self, surface):
        for tile in self.tilemap:
            tile.draw(surface)
        # for resource in self.resources:
        #     resource.draw(surface)
            


class Control(object):
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.done = False
        self.keys=pg.key.get_pressed()
        self.logictimer = 0
        self.drawtimer = 0

       
        self.player = Player((400,400))
        self.viewport = self.screen.get_rect()
        self.level = pg.Surface((c.mapWidth*c.tileSize,c.mapHeight*c.tileSize)).convert()
        self.level_rect = self.level.get_rect()

        
    def event_loop(self):
        inputcontroller.playerInput(self)

                
    def update(self,deltatime):
        t = time.time()
        self.player.update(self.world.obstacles, deltatime)
        spell_sprites.update(deltatime)
        character_sprites.update(self.world.obstacles, deltatime)
        resource_sprites.update(deltatime)
        self.update_viewport()
        
        self.logictimer +=deltatime
        if self.logictimer>1:
            print(str('logictimer: ') + str(time.time()-t))
            self.logictimer=0
        
    def update_viewport(self):
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.level_rect)
        
    def healthbars(self, screen):
        for enemy in character_sprites:
            length = 64*(enemy.healthCurrent/enemy.healthMax)
            pg.draw.rect(screen, c.red, (enemy.rect.x,enemy.rect.y-15,length,10))
            
    def workbars(self, screen):
        for resource in resource_sprites:
            if resource.jobTimer !=0:
                length = 64*(resource.jobTimer/resource.jobTime)
                pg.draw.rect(screen, c.blue, (resource.rect.x,resource.rect.y-15,length,10))
                    
    def draw(self, deltatime):
        t = time.time()
        self.world.draw(self.level)
        self.world.obstacles.draw(self.level)
        spell_sprites.draw(self.level)
        character_sprites.draw(self.level)
        resource_sprites.draw(self.level)
        self.player.draw(self.level)
        self.healthbars(self.level)
        self.workbars(self.level)
        self.screen.blit(self.level, (0,0), self.viewport)
        pg.display.update()
        

        self.drawtimer +=deltatime
        if self.drawtimer>1:
            print(str('drawtimer: ') + str(time.time()-t))
            self.drawtimer=0
        
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
    

    
   
    
    
    