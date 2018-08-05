import pygame as pg
from . import constants as c
from . import main as m

def playerInput(player,world):
    for event in pg.event.get():
        # print(event)
        if event.type == pg.QUIT:
            m.run=False
            pg.quit()
        elif event.type == pg.KEYDOWN:
            if(event.key == pg.K_RIGHT):
                if player.rect.x!= c.mapWidth-1:
                    player.rect.x +=1
                    player.direction = 1
                    
            if(event.key == pg.K_LEFT):
                if player.rect.x!= 0:
                    player.rect.x -= 1
                    player.direction = 3
                    
            if(event.key == pg.K_DOWN):
                if player.rect.y!= c.mapHeight-1:
                    player.rect.y+=1
                    player.direction = 2
                    
            if(event.key == pg.K_UP):
                if player.rect.y!=0:
                    player.rect.y -=1
                    player.direction = 2

             
            if(event.key == pg.K_SPACE):
                currentTile = world.tilemap[player.rect.y][player.rect.x]
                if currentTile.tileType!='Grass':
                    player.inventory[currentTile.tileType]+=1
                    world.tilemap[player.rect.y][player.rect.x].tileType= 'Grass'
                    currentTile.updateTile()
            # print(m.player.Pos)