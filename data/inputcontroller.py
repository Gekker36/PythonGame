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
                player.moveRight = True
                player.direction = 1
                    
            if(event.key == pg.K_LEFT):
                player.moveLeft = True
                player.direction = 3
                    
            if(event.key == pg.K_DOWN):
                player.moveDown = True
                player.direction = 2
                    
            if(event.key == pg.K_UP):
                player.moveUp = True
                player.direction = 0
            
            if(event.key == pg.K_1):
                player.castFireball()
                    
        elif event.type == pg.KEYUP:
            if(event.key == pg.K_RIGHT):
                if player.x!= c.mapWidth-1:
                    player.moveRight = False
                    player.direction = 1
                    
            if(event.key == pg.K_LEFT):
                if player.x!= 0:
                    player.moveLeft = False
                    player.direction = 3
                    
            if(event.key == pg.K_DOWN):
                if player.y!= c.mapHeight-1:
                    player.moveDown = False
                    player.direction = 2
                    
            if(event.key == pg.K_UP):
                if player.y!=0:
                    player.moveUp = False
                    player.direction = 0

             
            if(event.key == pg.K_SPACE):
                currentTile = world.tilemap[int(round(player.y))][int(round(player.x))]
                if currentTile.tileType!='Grass':
                    player.inventory[currentTile.tileType]+=1
                    world.tilemap[int(round(player.y))][int(round(player.x))].tileType= 'Grass'
                    currentTile.updateTile()
            # print(player.rect)