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
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.direction = 2
        self.inventory = {'Grass': 0, 'Water': 0, 'Stone': 0}

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

    def update_GUI(self,DISPLAYSURF, player):
        placePosition = 10
        
        
        #Draw resources
        for item in player.inventory:
            image = setup.TMX[item]
            rect = image.get_rect()
            surface = pg.Surface(rect.size)
            placePosition +=10
            textObj = self.font.render(str(player.inventory[item]), True, c.white, c.black)
            surface.blit(image, rect)
            surface.blit(textObj, rect)
            DISPLAYSURF.blit(surface,(placePosition,5))
            placePosition +=60
            
        

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
    
    DISPLAYSURF = pg.display.set_mode((c.mapWidth*c.tileSize, c.mapHeight*c.tileSize+50))
    pgClock = pg.time.Clock()
    
    print("Create world")
    world = World()
    
    print("Create player")
    player = Player()
    
    print("Create GUI")
    gui = GUI()
    # guiSurface = pg.Surface((0, 0))
    # DISPLAYSURF.blit(guiSurface, (0, 0))
    
    INVFONT=pg.font.SysFont('arial',18)
    
    print("Start gameplay loop")
    run=True
    
    '''
    Main gameloop
    '''
    
    while run:
    
        inputcontroller.playerInput(player, world)
    #     # fpsTimer=pgClock.tick(60)
                
        for row in range(c.mapHeight):
            for column in range(c.mapWidth):
                DISPLAYSURF.blit(world.tilemap[row][column].image,(column*c.tileSize,(row*c.tileSize)+50))
                
    
    
        
        DISPLAYSURF.blit(player.image, (player.rect.x*c.tileSize,player.rect.y*c.tileSize+50))
        gui.update_GUI(DISPLAYSURF,player)

         
        # gui.make_dialogue_box()
        # DISPLAYSURF.blit(player.image, (player.rect.x*c.tileSize,player.rect.y*c.tileSize+50))
        
        # # Draw GUI
        # placePosition = 10
        # for item in player.inventory:
        #     DISPLAYSURF.blit(setup.TMX[item], (placePosition, 5))
        #     placePosition += 50
        #     textObj = INVFONT.render(str(player.inventory[item]), True, c.white, c.black)
        #     DISPLAYSURF.blit(textObj, (placePosition,16))
        #     placePosition +=60
            
        # fpsClock = gui.render(str(int(pgClock.get_fps())), True, c.white, c.black)   
        # DISPLAYSURF.blit(fpsClock, (placePosition,16))
        pg.display.update()
    
    
    
    
    