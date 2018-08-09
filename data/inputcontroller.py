import pygame as pg
from . import constants as c
from . import main as m

def playerInput(gameControl):
    for event in pg.event.get():
        # print(event)
        if event.type == pg.QUIT:
            gameControl.quit=True
            
        elif event.type == pg.KEYDOWN:
            if(event.key == pg.K_RIGHT):
                gameControl.player.moveRight = True
                gameControl.player.direction = 1
                    
            if(event.key == pg.K_LEFT):
                gameControl.player.moveLeft = True
                gameControl.player.direction = 3
                    
            if(event.key == pg.K_DOWN):
                gameControl.player.moveDown = True
                gameControl.player.direction = 2
                    
            if(event.key == pg.K_UP):
                gameControl.player.moveUp = True
                gameControl.player.direction = 0
                
            if(event.key == pg.K_SPACE):
                currentTile = gameControl.world.tilemap[int(round(gameControl.player.rect.y))][int(round(gameControl.player.rect.x))]
                if currentTile.tileType!='Grass':
                    gameControl.player.inventory[currentTile.tileType]+=1
                    gameControl.world.tilemap[int(round(gameControl.player.rect.y))][int(round(gameControl.player.rect.x))].tileType= 'Grass'
            
            if(event.key == pg.K_1):
                gameControl.player.castFireball()
                
                    
        elif event.type == pg.KEYUP:
            if(event.key == pg.K_RIGHT):
                gameControl.player.moveRight = False
                    
                    
            if(event.key == pg.K_LEFT):
               gameControl.player.moveLeft = False
                    
                    
            if(event.key == pg.K_DOWN):
                gameControl.player.moveDown = False
                  
                    
            if(event.key == pg.K_UP):
                gameControl.player.moveUp = False
                    

             
        
            # print(player.rect)