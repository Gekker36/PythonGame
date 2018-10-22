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

    def draw_healthbars(self, screen):
        for enemy in m.character_sprites:
            if enemy.healthCurrent < enemy.healthMax:
                length = 64*(enemy.healthCurrent/enemy.healthMax)
                pg.draw.rect(screen, c.red, (enemy.rect.x,enemy.rect.y-15,length,10))
            
    def draw_workbars(self, screen):
        for resource in m.resource_sprites:
            if resource.jobTimer !=0:
                length = 64*(resource.jobTimer/resource.jobTime)
                pg.draw.rect(screen, c.blue, (resource.rect.x,resource.rect.y-15,length,10))
                
                
    def draw_inventory(self, level):
        if self.inventoryOpen:
            pg.draw.rect(level, c.white, (self.viewport.x+(self.viewport.width-200), self.viewport.y+(self.viewport.height)-300, 200,300))
            
            
            if len(self.control.world.player.inventory.items):
                position = 0
                for item in self.control.world.player.inventory.items:
                    textObj = self.font.render(str(item.name)+'x'+str(item.amount), True, c.black, c.white)
                    level.blit(textObj, (self.viewport.x+(self.viewport.width-200), self.viewport.y+(self.viewport.height)+position-300))
                    position += 20
            else:                
                textObj = self.font.render(str('Inventory is empty' ), True, c.black, c.white)
                level.blit(textObj, (self.viewport.x+(self.viewport.width-200), self.viewport.y+(self.viewport.height)-300))
                
                
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
    
    def draw_hotbar(self, screen):
        pg.display.get_surface().blit(setup.GFX['Empty_Inventory'].convert(), (100,100))
        
    def update(self):
        pass
        
    def draw(self, level, viewport):
        self.draw_healthbars(level)
        self.draw_workbars(level)
        self.draw_hotbar(level)
        self.draw_inventory(level)
        self.draw_charactersheet(level)

                    
                
    # print('test')