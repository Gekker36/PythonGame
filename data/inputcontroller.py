import pygame as pg
from . import constants as c
from . import main as m

def playerInput(player,world, deltatime):
    for event in pg.event.get():
        # print(event)
        if event.type == pg.QUIT:
            m.run=False
            pg.quit()
        elif event.type == pg.KEYDOWN:
            if(event.key == pg.K_RIGHT):
                if player.x!= c.mapWidth-1:
                    player.x +=1*deltatime
                    player.direction = 1
                    
            if(event.key == pg.K_LEFT):
                if player.x!= 0:
                    player.x -= 1*deltatime
                    player.direction = 3
                    
            if(event.key == pg.K_DOWN):
                if player.y!= c.mapHeight-1:
                    player.y+=1*deltatime
                    player.direction = 2
                    
            if(event.key == pg.K_UP):
                if player.y!=0:
                    player.y -=1*deltatime
                    player.direction = 2
                    
        elif event.type == pg.KEYUP:
            if(event.key == pg.K_RIGHT):
                if player.x!= c.mapWidth-1:
                    player.x +=1*deltatime
                    player.direction = 1
                    
            if(event.key == pg.K_LEFT):
                if player.x!= 0:
                    player.x -= 1*deltatime
                    player.direction = 3
                    
            if(event.key == pg.K_DOWN):
                if player.y!= c.mapHeight-1:
                    player.y+=1*deltatime
                    player.direction = 2
                    
            if(event.key == pg.K_UP):
                if player.y!=0:
                    player.y -=1*deltatime
                    player.direction = 2

             
            if(event.key == pg.K_SPACE):
                currentTile = world.tilemap[player.rect.y][player.rect.x]
                if currentTile.tileType!='Grass':
                    player.inventory[currentTile.tileType]+=1
                    world.tilemap[player.rect.y][player.rect.x].tileType= 'Grass'
                    currentTile.updateTile()
            # print(player.rect)