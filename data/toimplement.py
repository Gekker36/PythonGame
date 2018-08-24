
#         
# class Crop(pg.sprite.Sprite):        
#     def __init__(self,tile):
#         pg.sprite.Sprite.__init__(self, crop_sprites)
#         self.image = setup.GFX['Potato']
#         self.rect = self.image.get_rect()
#         self.rect.x = tile.rect.x
#         self.rect.y = tile.rect.y
#         self.type = ["Potato"]
#         self.growTime = 10
#         self.time = 0
#         self.canHarvest = False
#         
#     def update(self, deltatime):
#         if self.time < self.growTime:
#             self.time += deltatime
#         if self.time >= self.growTime:
#             self.canHarvest = True

 class Icon(pg.sprite.Sprite):
#     def __init__(self, base, inventory):
#         pg.sprite.Sprite.__init__(self, icon_sprites)
#         
#         self.item = base
#         self.image = self.item.image
#         self.rect = self.image.get_rect()
#         self.inventory = inventory
#         
    
# 
# class GUI(object):
#     def __init__(self):
#         self.font = pg.font.SysFont('arial',18)
#         self.playerInventory_shown = False
#         self.charactersheet_shown = False
#         self.mainmenu_shown = False
#         self.chestInventory_shown = False
#         
#     def floating_text(self, text, object):
#         print(text)
#         
#     def draw_TopGUI(self,player, fpsClock):
#         
#         #Draw Top GUI
#         placePosition = 10
#         screen = pg.Surface((c.mapWidth*c.tileSize, 100))
#         
#         #Draw Health
#         textObj = self.font.render(str('HEALTH: ') +str(int(player.healthCurrent)) + str(' / ') + str(int(player.healthMax)), True, c.white, c.black)
#         screen.blit(textObj, (placePosition, 5))
#         #Draw Mana
#         textObj = self.font.render(str('MANA: ') +str(int(player.manaCurrent)) + str(' / ') + str(int(player.manaMax)), True, c.white, c.black)
#         screen.blit(textObj, (placePosition, 25))
#         #Draw level
#         textObj = self.font.render(str('Level: ') +str(int(player.level)), True, c.white, c.black)
#         screen.blit(textObj, (placePosition, 45))
#         #Draw Experience
#         textObj = self.font.render(str('Experience: ') +str(int(player.experience)) , True, c.white, c.black)
#         screen.blit(textObj, (placePosition, 65))
#         
#         placePosition += 150
#         #Print FPS
#         textObj = self.font.render(str(fpsClock), True, c.white, c.black)
#         screen.blit(textObj, (placePosition, 5))
#         
#         #Print number of spell Sprites
#         textObj = self.font.render(str(len(spell_sprites)), True, c.white, c.black)
#         screen.blit(textObj, (placePosition, 25))
#         
#         #Print number of icon Sprites
#         textObj = self.font.render(str(len(icon_sprites)), True, c.white, c.black)
#         screen.blit(textObj, (placePosition, 45))
#         
#         return screen
# 
# 
#     def draw_CharacterScreen(self, player):
#         pass
#         
#     
#     def update_GUI(self,DISPLAYSURF, player, fpsClock):
#         
#         screen = self.draw_TopGUI(player,fpsClock)
#         DISPLAYSURF.blit(screen,(0,0))
#         
#         
#         icon_sprites.empty()
#         #Draw inventory screen
#         if self.playerInventory_shown:
#             #Draw own inventory
#             placepositionx = 0
#             placepositiony = 0
#             
#             playerInventorySurface = pg.Surface((128,320))
#             playerInventorySurface.fill(c.white)
#             
#             #Draw player inventory  
#             #Draw empty spots
#             for i in range(player.inventory.size):
#                 playerInventorySurface.blit(setup.GFX["Empty Inventory"], (placepositionx,placepositiony))
#                 placepositiony += 64
#                 if placepositiony >= 320:
#                     placepositiony = 0
#                     placepositionx += 64
#                     
#                     
#             #Draw filled spots      
#             placepositionx = 0
#             placepositiony = 0
#             for item in player.inventory.items:
#                 icon=Icon(item, player.inventory)
#                 playerInventorySurface.blit(icon.image, (placepositionx,placepositiony))
#                 icon.rect.x = placepositionx+512
#                 icon.rect.y = placepositiony
#                 placepositiony += 64
#                 if placepositiony >= 320:
#                     placepositiony = 0
#                     placepositionx += 64
#             DISPLAYSURF.blit(playerInventorySurface,(512,100))
#             
#             
#             #Draw chest inventory 
#             
# 
#             if len(player.colliders)>=1:
#                 
#                 chestInventorySurface = pg.Surface((128,320))
#                 chestInventorySurface.fill(c.white)
#                 placepositionx = 0
#                 placepositiony = 0
#                     
#                 for i in range(player.inventory.size):
#                     chestInventorySurface.blit(setup.GFX["Empty Inventory"], (placepositionx,placepositiony))
#                     placepositiony += 64
#                     if placepositiony >= 320:
#                         placepositiony = 0
#                         placepositionx += 64
#                         
#                         
#                 placepositionx = 0
#                 placepositiony = 0
#                 for item in player.colliders[0].inventory.items:
#                     icon=Icon(item, player.colliders[0].inventory)
#                     chestInventorySurface.blit(icon.image, (placepositionx,placepositiony))
#                     icon.rect.x = placepositionx+320
#                     icon.rect.y = placepositiony+100
#                     placepositiony += 64
#                     if placepositiony >= 320:
#                         placepositiony = 0
#                         placepositionx += 64
#                 DISPLAYSURF.blit(chestInventorySurface,(320,100))
#                 
# 
#         #Draw CharacterSheet screen
#         if self.charactersheet_shown:
# 
#             placepositionx = 0
#             placepositiony = 0
#             
#             characterSheetSurface = pg.Surface((124,400))
#             characterSheetSurface.fill(c.white)
#             
#             for key in player.equipped:
#                 textObj = self.font.render(str(key), True, c.white, c.black)
#                 characterSheetSurface.blit(textObj, (placepositionx, placepositiony))
#                 placepositiony +=20
#                 
#                 if player.equipped[key]:
#                     icon=Icon(player.equipped[key], player.equipped)
#                     icon.rect.x = placepositionx
#                     icon.rect.y = placepositiony
#                     characterSheetSurface.blit(icon.image, (placepositionx, placepositiony))
#                     
#                 else:
#                     characterSheetSurface.blit(setup.GFX["Empty Inventory"], (placepositionx, placepositiony))
#                 placepositiony +=80
#             
#             DISPLAYSURF.blit(characterSheetSurface,(0,100))
#         
#         #Draw MainMenu
#         if self.mainmenu_shown:
#             square = pg.draw.rec