from data.states import  level #, death, shop, levels, battle,
# from data.states import credits
from . import setup, tools, inputcontroller, player
from . import constants as c
import pygame as pg
import random
import math

tile_sprites = pg.sprite.Group()
# crop_sprites = pg.sprite.Group()
# character_sprites = pg.sprite.Group()
# object_sprites = pg.sprite.Group()
# spell_sprites = pg.sprite.Group()
# icon_sprites = pg.sprite.Group()

ANGLE_UNIT_SPEED = math.sqrt(2)/2
DIRECT_DICT = {pg.K_LEFT  : (-1, 0),
               pg.K_RIGHT : ( 1, 0),
               pg.K_UP    : ( 0,-1),
               pg.K_DOWN  : ( 0, 1)}


class Player(pg.sprite.Sprite):
    def __init__(self, location, direction=pg.K_RIGHT):
        # pg.sprite.Sprite.__init__(self,character_sprites)
        self.image = setup.GFX['Potato']
        # self.image.convert_alpha()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(topleft = location)

        self.colliders=[]
        
        
        self.true_pos = list(self.rect.center)
        self.remainder = [0, 0]  #Adjust rect in integers; save remainders.
        self.direction = direction
        self.old_direction = None  #The Players previous direction every frame.
        self.direction_stack = []  #Held keys in the order they were pressed.
        self.redraw = False  #Force redraw if needed.
        
        self.moveSpeed = 500
        # self.inventory = Inventory()
        self.healthCurrent = 100
        self.healthMax = 100
        self.healthRegen = 1
        self.manaCurrent = 50
        self.manaMax = 100
        self.manaRegen = 10
        
        self.level = 1
        self.experience = 0
        
        
        self.equipped = {"Head":[], "Body":[], "Weapon":[], "Shield":[]}
        self.attack = 10
        self.defence = 10
        
        
        
    # def castFireball(self):
    #     print("Casting Fireball")
    #     Spell(self)
    # 
    # def createChest(self):
    #     print("Creating Chest")
    #     Chest(self)
    #   
    # def createItem(self):
    #     self.inventory.add_item(Item())
    #     
    # def gainExperience(self, experience):
    #     self.experience += experience
            
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
        frame_speed = self.moveSpeed*factor*deltatime
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
        
        
class Block(pg.sprite.Sprite):
    """Something to run head-first into."""
    def __init__(self, location):
        """The location argument is where I will be located."""
        pg.sprite.Sprite.__init__(self)
        self.image = setup.GFX['stone_block']
        self.rect = self.image.get_rect(topleft = location)
        self.mask = pg.mask.from_surface(self.image)

        
class Tile(pg.sprite.Sprite):
    def __init__(self,x,y,tileType):
        pg.sprite.Sprite.__init__(self, tile_sprites)
        self.tileType = tileType
        self.image = setup.TMX[tileType]
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
        
    def draw(self, surface):
        surface.blit(self.image, self.rect+64)
        
        if self.hasCrop:
            surface.blit(self.crop.image, self.crop.rect)
        
        
class World(object):
    def __init__(self,viewport):
        self.mapHeight = c.mapHeight
        self.mapWidth = c.mapWidth
        self.tileSize = c.tileSize
        self.worldGenerator()
    
    def worldGenerator(self):
        print("Create tilemap")
        self.tilemap = [[Tile(w,h,'Grass') for w in range(self.mapWidth)] for h in range(self.mapHeight)]
        self.obstacles = pg.sprite.Group([Block((64*5,64*8)), Block((64*9,64*6)), Block((64*3,64*1))])
        
        for h in range(self.mapHeight):
            for w in range(self.mapWidth):
                if random.randint(1,100)<15 :
                    self.tilemap[h][w]= Tile(w,h,'Water')
                if random.randint(1,100)<15 :
                    self.tilemap[h][w]= Tile(w,h,'Stone')


class Control(object):
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.done = False
        self.keys=pg.key.get_pressed()
        

       
        self.player = Player((400,400))
        self.viewport = self.screen.get_rect()
        self.level = pg.Surface((5000,5000)).convert()
        self.level_rect = self.level.get_rect()

        
    def event_loop(self):
        for event in pg.event.get():
            self.keys = pg.key.get_pressed()
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.player.add_direction(event.key)
            elif event.type == pg.KEYUP:
                self.player.pop_direction(event.key)
                
    def update(self,deltatime):
        self.player.update(self.world.obstacles, deltatime)
        self.update_viewport()
        
    def update_viewport(self):
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.level_rect)
        
    def draw(self):
        # self.level.fill(pg.Color("lightblue"))
        tile_sprites.draw(self.level)
        self.world.obstacles.draw(self.level)
        self.player.draw(self.level)
        self.screen.blit(self.level, (0,0), self.viewport)
        pg.display.update()

    def display_fps(self):
        """Show the program's FPS in the window handle."""
        caption = "{} - FPS: {:.2f}".format("Test Pygame", int(self.clock.get_fps()))
        pg.display.set_caption(caption)
        
  
    def main(self):

        print("Create world")
        self.world = World(self.screen_rect.copy())

        print("Starting main loop")
        while not self.done:
            self.deltatime = self.clock.tick(60)/1000
            self.event_loop()
            self.update(self.deltatime)
            self.draw()
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
    

    
   
    
    
    