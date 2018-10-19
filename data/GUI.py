import pygame as pg
from . import constants as c
from . import main as m
from . import setup




class GUI(object):
    def __init__(self):
        self.inventoryOpen = False
        self.charactersheetOpen = False

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
        
    def draw(self, screen):
        self.draw_healthbars(screen)
        self.draw_workbars(screen)
        self.draw_hotbar(screen)
                    
                
    # print('test')