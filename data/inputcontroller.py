import pygame as pg
from . import constants as c
from . import main as m

def playerInput(gameControl):
    for event in pg.event.get():
        # print(event)
        if event.type == pg.QUIT:
            gameControl.quit=True
        
        elif event.type == pg.MOUSEBUTTONDOWN:
            mousePos = pg.mouse.get_pos()
            mouseColliders = [s for s in m.icon_sprites if s.rect.collidepoint(mousePos)]
            if mouseColliders:
                if gameControl.player.colliders:
                    if mouseColliders[0].inventory == gameControl.player.inventory:
                        gameControl.player.colliders[0].inventory.add_item(mouseColliders[0].item)
                        gameControl.player.inventory.remove_item(mouseColliders[0].item)
                    
                    elif mouseColliders[0].inventory == gameControl.player.colliders[0].inventory:
                        gameControl.player.colliders[0].inventory.remove_item(mouseColliders[0].item)
                        gameControl.player.inventory.add_item(mouseColliders[0].item)
                        
                    
                elif mouseColliders[0].inventory == gameControl.player.equipped:
                    gameControl.player.equipped[mouseColliders[0].item.type] = []
                    gameControl.player.inventory.add_item(mouseColliders[0].item) 
                      
                else:
                    gameControl.player.equipped[mouseColliders[0].item.type] = mouseColliders[0].item
                    gameControl.player.inventory.remove_item(mouseColliders[0].item)
                
                
                        
                        
                        
            
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
                
            # if(event.key == pg.K_SPACE):
            #     currentTile = gameControl.world.tilemap[int(round((gameControl.player.rect.y-100)/64))][int(round(gameControl.player.rect.x/64))]
            #     if currentTile.tileType!='Grass':
            #         gameControl.player.inventory[currentTile.tileType]+=1
            #         gameControl.world.tilemap[int(round((gameControl.player.rect.y-100)/64))][int(round(gameControl.player.rect.x/64))].tileType= 'Grass'
            
            if(event.key == pg.K_1):
                gameControl.player.castFireball()
              
            if(event.key == pg.K_2):
                gameControl.player.createItem()
                
            if(event.key == pg.K_3):
                gameControl.player.createChest()
                
            if(event.key == pg.K_4):
                print(gameControl.player.itemInventory.items) 
                
            if(event.key == pg.K_5):
                m.Enemy()
               
            if(event.key == pg.K_i):
                gameControl.gui.playerInventory_shown= not gameControl.gui.playerInventory_shown
                
            if(event.key == pg.K_c):
                gameControl.gui.charactersheet_shown= not gameControl.gui.charactersheet_shown
                    
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