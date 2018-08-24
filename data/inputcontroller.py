import pygame as pg
from . import constants as c
from . import main as m

def playerInput(control):
    for event in pg.event.get():
        # print(event)
        if  (event.type == pg.QUIT):
            control.done = True
            
        # elif event.type == pg.MOUSEBUTTONDOWN:
        #     mousePos = pg.mouse.get_pos()
        #     mouseColliders = [s for s in m.icon_sprites if s.rect.collidepoint(mousePos)]
        #     if mouseColliders:
        #         if gameControl.player.colliders:
        #             if mouseColliders[0].inventory == gameControl.player.inventory:
        #                 gameControl.player.colliders[0].inventory.add_item(mouseColliders[0].item)
        #                 gameControl.player.inventory.remove_item(mouseColliders[0].item)
        #             
        #             elif mouseColliders[0].inventory == gameControl.player.colliders[0].inventory:
        #                 gameControl.player.colliders[0].inventory.remove_item(mouseColliders[0].item)
        #                 gameControl.player.inventory.add_item(mouseColliders[0].item)
        #                 
        #             
        #         elif mouseColliders[0].inventory == gameControl.player.equipped:
        #             gameControl.player.equipped[mouseColliders[0].item.type] = []
        #             gameControl.player.inventory.add_item(mouseColliders[0].item) 
        #               
        #         else:
        #             gameControl.player.equipped[mouseColliders[0].item.type] = mouseColliders[0].item
        #             gameControl.player.inventory.remove_item(mouseColliders[0].item)
                
                
                        
                        
                        
            
        elif event.type == pg.KEYDOWN:
            if(event.key == pg.K_RIGHT) or (event.key == pg.K_LEFT) or (event.key == pg.K_DOWN) or (event.key == pg.K_UP):
                control.player.add_direction(event.key)
                
            # if(event.key == pg.K_SPACE):
            #     currentTile = gameControl.world.tilemap[int(round((gameControl.player.rect.y-100)/64))][int(round(gameControl.player.rect.x/64))]
            #     if not currentTile.hasCrop:
            #         currentTile.plant_crop(m.Crop(currentTile))

             
            if(event.key == pg.K_1):
                control.player.castFireball()
              
            if(event.key == pg.K_2):
                mousePos = pg.mouse.get_pos()
                worldPos = mousePos[0]+control.viewport[0],mousePos[1]+control.viewport[1]
                m.Enemy(worldPos,control.world)
                
            if(event.key == pg.K_3):
                mousePos= pg.mouse.get_pos()
                worldPos = [mousePos[0]+control.viewport.x, mousePos[1]+control.viewport.y]
                
                mouseColliders = [s for s in control.world.tilemap if s.rect.collidepoint(worldPos)]
                currentTile = mouseColliders[0]
                control.world.generate_resource(currentTile)
                
            if(event.key == pg.K_4):
                mousePos= pg.mouse.get_pos()
                worldPos = [mousePos[0]+control.viewport.x, mousePos[1]+control.viewport.y]
                
                mouseColliders = [s for s in control.world.tilemap if s.rect.collidepoint(worldPos)]
                currentTile = mouseColliders[0]
                control.world.create_chest(currentTile)
                
            if(event.key == pg.K_e):
                control.player.working = True
            #     
            #  
            #     
            # if(event.key == pg.K_5):
            #     m.Enemy()
            #    
            # if(event.key == pg.K_i):
            #     gameControl.gui.playerInventory_shown= not gameControl.gui.playerInventory_shown
            #     
            # if(event.key == pg.K_c):
            #     gameControl.gui.charactersheet_shown= not gameControl.gui.charactersheet_shown
                    
        elif event.type == pg.KEYUP:
            if(event.key == pg.K_RIGHT) or (event.key == pg.K_LEFT) or (event.key == pg.K_DOWN) or (event.key == pg.K_UP):
                control.player.pop_direction(event.key)
                    
            if(event.key == pg.K_e):
                control.player.working = False

             
        
            # print(player.rect)