import pygame as pg
from . import constants as c
from . import main as m
from . import setup




class GUI(object):
    def __init__(self, viewport,control):
        self.inventoryOpen = False
        self.charactersheetOpen = False
        self.viewport = viewport
        self.control = control
        self.font = pg.font.SysFont('arial',18)
        self.hotbarSelected = 1

    def draw_healthbars(self, screen):
        for enemy in self.control.world.character_sprites:
            if enemy.healthCurrent < enemy.healthMax:
                length = 64*(enemy.healthCurrent/enemy.healthMax)
                pg.draw.rect(screen, c.red, (enemy.rect.x,enemy.rect.y-15,length,10))
            
    def draw_workbars(self, screen):
        for resource in self.control.world.resource_sprites:
            if resource.jobTimer !=0:
                length = 64*(resource.jobTimer/resource.jobTime)
                pg.draw.rect(screen, c.blue, (resource.rect.x,resource.rect.y-15,length,10))
                
                
    def draw_inventory(self, level):
        if self.inventoryOpen: #Draw own inventory
            pg.draw.rect(level, c.white, (self.viewport.x+(self.viewport.width-200), self.viewport.y+(self.viewport.height)-364, 200,300))
            
            
            if len(self.control.world.player.inventory.items):
                position = 0
                for item in self.control.world.player.inventory.items:
                    textObj = self.font.render(str(item.name)+'x'+str(item.amount), True, c.black, c.white)
                    level.blit(textObj, (self.viewport.x+(self.viewport.width-200), self.viewport.y+(self.viewport.height)+position-364))
                    position += 20
            else:                
                textObj = self.font.render(str('Inventory is empty' ), True, c.black, c.white)
                level.blit(textObj, (self.viewport.x+(self.viewport.width-200), self.viewport.y+(self.viewport.height)-364))
                
                
                
            hit = pg.sprite.spritecollide(self.control.world.player, self.control.world.object_sprites, False)
        
            if hit and isinstance(hit[0],m.Chest): #Draw chest inventory
                pg.draw.rect(level, c.white, (self.viewport.x+(self.viewport.width-450), self.viewport.y+(self.viewport.height)-364, 200,300))
                if len(hit[0].inventory.items):
                    position = 0
                    for item in hit[0].inventory.items:
                        textObj = self.font.render(str(item.name)+'x'+str(item.amount), True, c.black, c.white)
                        level.blit(textObj, (self.viewport.x+(self.viewport.width-450), self.viewport.y+(self.viewport.height)+position-364))
                        position += 20
                
        
                
                
    def draw_charactersheet(self, level):
        if self.charactersheetOpen:
            player = self.control.world.player
            position = 0
            
            pg.draw.rect(level, c.white, (self.viewport.x+(self.viewport.width-200), self.viewport.y, 200,400))
            statlist= ['healthCurrent', 'healthMax', 'manaCurrent', 'manaMax', 'movespeed', 'level', 'experience']
            
            for stat in statlist:
                textObj = self.font.render(str(stat) + ' : ' + str(player.__getattribute__(stat)), True, c.black, c.white)
                level.blit(textObj, (self.viewport.x+(self.viewport.width-200), self.viewport.y+position))
                position += 20
        
            for equipment in player.equipped:
                textObj = self.font.render(str(equipment), True, c.black, c.white)
                level.blit(textObj, (self.viewport.x+(self.viewport.width-200), self.viewport.y+position))
                position += 20
            
    def draw_hotbar(self, level):
        position = 112
        for i in range(9):
            if i == self.hotbarSelected-1:
                level.blit(setup.GFX['Hotbar_Selected'], (self.viewport.x + position, self.viewport.y+(self.viewport.height)-64))
                textObj = self.font.render(str(i+1), True, c.white, c.red)
            else:
                level.blit(setup.GFX['Empty_Inventory'].convert(), (self.viewport.x + position, self.viewport.y+(self.viewport.height)-64))
                textObj = self.font.render(str(i+1), True, c.white, c.blue)
            level.blit(textObj, (self.viewport.x + position, self.viewport.y+(self.viewport.height)-64))
            position += 64
        
        
             
    def openInventory(self):
        if self.inventoryOpen:
            print('Closing invenventory')
        if not self.inventoryOpen:
            print('Opening inventory')
        self.inventoryOpen = not self.inventoryOpen
        
        
    def openCharacterScreen(self):
        if self.charactersheetOpen:
            print('Closing Character Screen')
        if not self.charactersheetOpen:
            print('Opening Character Screen')
        self.charactersheetOpen = not self.charactersheetOpen
    

        
    def update(self):
        pass
        
    def draw(self, level, viewport):
        self.draw_healthbars(level)
        self.draw_workbars(level)
        self.draw_hotbar(level)
        self.draw_inventory(level)
        self.draw_charactersheet(level)

                    
                
    # print('test')