from data.states import  level #, death, shop, levels, battle,
# from data.states import credits
from . import setup, tools, inputcontroller, player
from . import constants as c
import pygame as pg
import random

tile_sprites = pg.sprite.Group()
character_sprites = pg.sprite.Group()
spell_sprites = pg.sprite.Group()


class Player(object):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = setup.GFX['Character']
        self.image.convert_alpha()
        self.image.set_colorkey((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.x = 5
        self.y = 5
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False
        
        self.direction = 2
        self.inventory = {'Grass': 0, 'Water': 0, 'Stone': 0}
        self.healthCurrent = 100
        self.healthMax = 100
        self.healthRegen = 1
        self.manaCurrent = 50
        self.manaMax = 100
        self.manaRegen = 10
        self.moveSpeed = 2
        
    def castFireball(self):
        print("Casting Fireball")
        Spell(self)
        
    
    def updatePlayer(self, DISPLAYSURF, deltatime):
        
        if self.healthCurrent < self.healthMax:
            self.healthCurrent += (self.healthRegen*deltatime)
        if self.manaCurrent < self.manaMax:
            self.manaCurrent += (self.manaRegen*deltatime)  
            
        if self.moveLeft == True:
            if self.x >= 0:
                self.x -=self.moveSpeed*deltatime
            
        if self.moveRight == True:
            if self.x <= c.mapWidth-1:
                self.x += self.moveSpeed*deltatime
               
        if self.moveUp == True:
            if self.y>= 0:
                self.y -= self.moveSpeed*deltatime
                   
        if self.moveDown == True:
            if self.y <= c.mapHeight-1:
                self.y +=self.moveSpeed*deltatime 
            
        DISPLAYSURF.blit(self.image, (self.x*c.tileSize,self.y*c.tileSize+100))
        
class Spell(pg.sprite.Sprite):
    def __init__(self, player):
        self.manaCost = 10
        if player.manaCurrent >= self.manaCost:
            pg.sprite.Sprite.__init__(self,spell_sprites)
            self.image = setup.GFX['Orb of Flame']
            self.rect = self.image.get_rect()
            self.rect.x = player.x*64
            self.rect.y = (player.y*64)+100
            self.image.set_colorkey((0,0,0))
            self.direction = player.direction
            self.speed = 4
            player.manaCurrent -= self.manaCost
            
    def update(self, deltatime):
        
        if self.direction == 0:
            # self.rect.x += self.speed
            self.rect.y -= self.speed
        if self.direction == 1:
            self.rect.x += self.speed
            # self.rect.y += self.speed
        if self.direction == 2:
            # self.rect.x += self.speed
            self.rect.y += self.speed
        if self.direction == 3:
            self.rect.x -= self.speed
            # self.rect.y += self.speed
            
        if self.rect.x >= c.mapWidth*c.tileSize or self.rect.x <= -c.tileSize or self.rect.y >= c.mapHeight*c.tileSize or self.rect.y <= -c.tileSize:
            self.kill()
       


    
    def draw(self, screen):
        surface.blit(self.image, self.rect)
        
        

class Tile(pg.sprite.Sprite):
    def __init__(self,x,y,tileType):
        pg.sprite.Sprite.__init__(self, tile_sprites)
        self.tileType = tileType
        self.image = setup.TMX[tileType]
        self.rect = self.image.get_rect()
        self.rect.x = x*64
        self.rect.y = (y*64)+100

        
    def update(self):
        self.image = setup.TMX[self.tileType]
        
    def draw(self,surface):
        surface.blit(self.image, self.rect+64)

        
        
class World(object):
    def __init__(self):
        self.mapHeight = c.mapHeight
        self.mapWidth = c.mapWidth
        self.tileSize = c.tileSize
        self.worldGenerator()
        self.tilemap
        
    
    def worldGenerator(self):
        print("Create tilemap")
        self.tilemap = [[Tile(w,h,'Grass') for w in range(self.mapWidth)] for h in range(self.mapHeight)]
        
        for h in range(self.mapHeight):
            for w in range(self.mapWidth):
                if random.randint(1,100)<15 :
                    self.tilemap[h][w]= Tile(w,h,'Water')
                if random.randint(1,100)<15 :
                    self.tilemap[h][w]= Tile(w,h,'Stone')

class GUI(object):
    def __init__(self):
        self.font = pg.font.SysFont('arial',18)

    def update_GUI(self,DISPLAYSURF, player, fpsClock):
        placePosition = 10
        
        GUIsurface = pg.Surface((c.mapWidth*c.tileSize, 100))
        
        #Draw Health
        textObj = self.font.render(str('HEALTH: ') +str(int(player.healthCurrent)) + str(' / ') + str(int(player.healthMax)), True, c.white, c.black)
        GUIsurface.blit(textObj, (placePosition, 5))
        #Draw Mana
        textObj = self.font.render(str('MANA: ') +str(int(player.manaCurrent)) + str(' / ') + str(int(player.manaMax)), True, c.white, c.black)
        GUIsurface.blit(textObj, (placePosition, 40))
        placePosition += 150
        
        #Draw resources
        for item in player.inventory:
            image = setup.TMX[item]
        
            textObj = self.font.render(str(player.inventory[item]), True, c.white, c.black)
            GUIsurface.blit(image, (placePosition,5))
            GUIsurface.blit(textObj, (placePosition,5))
            placePosition +=70
            
            
        textObj = self.font.render(str(fpsClock), True, c.white, c.black)
        GUIsurface.blit(textObj, (placePosition, 5))
        
        textObj = self.font.render(str(len(spell_sprites)), True, c.white, c.black)
        GUIsurface.blit(textObj, (placePosition, 40))
        
        DISPLAYSURF.blit(GUIsurface,(0,0))

    def make_dialogue_box(self):
        image = setup.TMX['Stone']
        rect = image.get_rect()
        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.black)
        surface.blit(image, rect)
        surface.blit(image, rect)
        dialogue = self.font.render("Schrijf hier text",
                                    True,
                                    c.black)
        dialogue_rect = dialogue.get_rect(left=50, top=50)
        surface.blit(dialogue, dialogue_rect)
        sprite = pg.sprite.Sprite()
        sprite.image = surface
        sprite.rect = rect
        return sprite
        

class GameControl(object):
    def __init__(self):
        self.screen = setup.SCREEN
        self.screen_rect = setup.SCREEN_RECT
        self.clock = pg.time.Clock()
        self.quit = False
        
        
        
    def update_events(self):
        inputcontroller.playerInput(self)
        tile_sprites.update()
        spell_sprites.update(self.deltatime)
        
        
    def update_screen(self):
        # for row in range(c.mapHeight):
        #     for column in range(c.mapWidth):
        #         self.screen.blit(self.world.tilemap[row][column].image,(column*c.tileSize,row*c.tileSize+100))
                
        tile_sprites.draw(self.screen)
        
        self.player.updatePlayer(self.screen,self.deltatime)
        spell_sprites.draw(self.screen)
        self.gui.update_GUI(self.screen,self.player,self.fpsClock)
        
        
    def main(self):
        print("GameControl init")
        
        # print("Create sprite group")
        # sprites = pg.sprite.Group()
        
        print("Create world")
        self.world = World()
        
        print("Create player")
        self.player = Player()
        
        print("Create GUI")
        self.gui = GUI()
        
        print("Starting main loop")
        while not self.quit:
            self.deltatime = self.clock.tick()/1000
            self.fpsClock = self.clock.get_fps()
            
            #Update game events
            self.update_events()
            
            #Draw game sprites
            self.update_screen()
            
            pg.display.update()
        
        
        

def main():
    
    print("Create GameControl")
    gameControl = GameControl().main()
    

    
   
    
    
    