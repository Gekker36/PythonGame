from data.states import  level #, death, shop, levels, battle,
# from data.states import credits
from . import setup, tools, inputcontroller, worldgenerator, player
from . import constants as c
import pygame as pg
import random


LEVEL ='level'
TOWN = 'town'

INVFONT=pg.font.SysFont('arial',18)



def main():
    """Add states to control here"""
    
    
print("Loading images")
tile_grass = setup.TMX['Grass']
tile_water = setup.TMX['Water']
tile_stone = setup.TMX['Stone']
# player = setup.GFX['Player']
bullet = setup.GFX['Bullet']


tileSize = 40

grass = 0
water = 1
stone = 2
resources = [grass, water, stone]
tileTextures = {grass:tile_grass, water: tile_water, stone: tile_stone}

white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
blue = (0,0,255)
brown = (153,76,0)



        

# playerPos = [int(c.mapWidth/2),int(c.mapHeight/2)]
inventory = {grass: 0, water: 0, stone: 0}


DISPLAYSURF = pg.display.set_mode((c.mapWidth*tileSize, c.mapHeight*tileSize+50))



# for row in range(c.mapHeight):
#     for column in range(c.mapWidth):
#         DISPLAYSURF.blit(tileTextures[tilemap[row][column]],(column*tileSize,(row*tileSize)+50))
   
pgClock = pg.time.Clock()

class Player(object):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = setup.GFX['Player']
        self.image.convert_alpha()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.direction = 2

class Tile(object):
    def __init__(self,x,y,tileType):
        pg.sprite.Sprite.__init__(self)
        self.tileType = tileType
        self.image = tileTextures[self.tileType]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



tilemap = [[Tile(w,h,0) for w in range(c.mapWidth)] for h in range(c.mapHeight)]

for h in range(c.mapHeight):
    for w in range(c.mapWidth):
        if random.randint(1,100)<15 :
            tilemap[h][w]= Tile(w,h,1)
        # if random.randint(1,100)<15 :
        #     tilemap[h][w]= m.Tile(w,h,0)

player = Player()
 

run=True
while run:

    inputcontroller.playerInput()
    fpsTimer=pgClock.tick(60)
            
    for row in range(c.mapHeight):
        for column in range(c.mapWidth):
            DISPLAYSURF.blit(tilemap[row][column].image,(column*tileSize,(row*tileSize)+50))
            
   

    
    DISPLAYSURF.blit(player.image, (player.rect.x*tileSize,player.rect.y*tileSize+50))
    
    # Draw GUI
    placePosition = 10
    for item in resources:
        DISPLAYSURF.blit(tileTextures[item], (placePosition, 5))
        placePosition += 50
        textObj = INVFONT.render(str(inventory[item]), True, white, black)
        fpsClock = INVFONT.render(str(int(pgClock.get_fps())), True, white, black)
        DISPLAYSURF.blit(textObj, (placePosition,16))
        placePosition +=60
        
    DISPLAYSURF.blit(fpsClock, (placePosition,16))
    pg.display.update()
    

    