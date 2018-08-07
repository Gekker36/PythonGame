from data.states import  level #, death, shop, levels, battle,
# from data.states import credits
from . import setup, tools, inputcontroller, player
from . import constants as c
import pygame as pg
import random




class Player(object):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = setup.GFX['Character']
        self.image.convert_alpha()
        self.image.set_colorkey((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.x = 0
        self.y = 0
        
        self.direction = 2
        self.inventory = {'Grass': 0, 'Water': 0, 'Stone': 0}
        self.healthCurrent = 100
        self.healthMax = 100
        self.healthRegen = 1
        self.manaCurrent = 50
        self.manaMax = 100
        self.manaRegen = 1
        self.moveSpeed = 1
    
    def updatePlayer(self, DISPLAYSURF, deltatime):
        
        if self.healthCurrent < self.healthMax:
            self.healthCurrent += (self.healthRegen*deltatime)
        if self.manaCurrent < self.manaMax:
            self.manaCurrent += (self.manaRegen*deltatime)  
            
        DISPLAYSURF.blit(self.image, (self.x*c.tileSize,self.y*c.tileSize+100))

        

class Tile(object):
    def __init__(self,x,y,tileType):
        pg.sprite.Sprite.__init__(self)
        self.tileType = tileType
        self.image = setup.TMX[tileType]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def updateTile(self):
        self.image = setup.TMX[self.tileType]
        
        
class World(object):
    def __init__(self):
        self.mapHeight = c.mapHeight
        self.mapWidth = c.mapWidth
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
        

    

def main():
    
    print("Starting Main")
    
    DISPLAYSURF = pg.display.set_mode((c.mapWidth*c.tileSize, c.mapHeight*c.tileSize+100))
    gameClock = pg.time.Clock()
    
    print("Create world")
    world = World()
    
    print("Create player")
    player = Player()
    
    print("Create GUI")
    gui = GUI()

    
    INVFONT=pg.font.SysFont('arial',18)
    
    print("Start gameplay loop")
    run=True
    
    '''
    Main gameloop
    '''
    
    while run:
        deltatime = gameClock.tick()/1000
        fpsClock = int(gameClock.get_fps())
    
        inputcontroller.playerInput(player, world, deltatime)
                
        for row in range(c.mapHeight):
            for column in range(c.mapWidth):
                DISPLAYSURF.blit(world.tilemap[row][column].image,(column*c.tileSize,row*c.tileSize+100))
                
        
        player.updatePlayer(DISPLAYSURF,deltatime)
        gui.update_GUI(DISPLAYSURF,player,fpsClock)

         
        pg.display.update()
    
    
    
    
    