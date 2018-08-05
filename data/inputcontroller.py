import pygame as pg
from . import constants as c
from . import main as m

def playerInput():
    x=0
    y=0
    for event in pg.event.get():
        # print(event)
        if event.type == pg.QUIT:
            m.run=False
        elif event.type == pg.KEYDOWN:
            if(event.key == pg.K_RIGHT):
                if m.player.rect.x!= c.mapWidth-1:
                    m.player.rect.x +=1
                    m.player.direction = 1
                    
            if(event.key == pg.K_LEFT):
                if m.player.rect.x!= 0:
                    m.player.rect.x -= 1
                    m.player.direction = 3
                    
            if(event.key == pg.K_DOWN):
                if m.player.rect.y!= c.mapHeight-1:
                    m.player.rect.y+=1
                    m.player.direction = 2
                    
            if(event.key == pg.K_UP):
                if m.player.rect.y!=0:
                    m.player.rect.y -=1
                    m.player.direction = 2

            
            if(event.key == pg.K_SPACE):
                currentTile = m.tilemap[m.player.rect.y][m.player.rect.x]
                if currentTile.tileType!=c.grass:
                    m.inventory[currentTile.tileType]+=1
                    # m.tilemap[m.player.rect.y][m.player.rect.x].tileType=c.grass
            # print(m.player.Pos)