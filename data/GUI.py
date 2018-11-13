import pygame as pg
import math
from . import constants as c
from . import settings as s
from . import main as m
from . import setup




class GUI(object):
    def __init__(self, control):
        
        self.menu_stack = []
        self.mainMenuOpen = False
        self.mainMenuSelection=0
        self.inventoryOpen = False
        self.inventorySelection = 0
        self.charactersheetOpen = False
        self.craftingOpen =  False
        self.mousePos = [0,0]
        self.control = control
        self.viewport = control.viewport
        self.level = control.level
        self.font = pg.font.SysFont('arial',18)
        self.hotbarSelected = 1
            
    def toggleMainMenu(self):
        if any(isinstance(menu, MainMenu) for menu in self.menu_stack):
            for menu in self.menu_stack:
                if isinstance(menu, MainMenu):
                    self.menu_stack.remove(menu)
        else:
            self.menu_stack.append(MainMenu(self))
        
    def toggleOptionsMenu(self):
        if any(isinstance(menu, OptionsMenu) for menu in self.menu_stack):
            for menu in self.menu_stack:
                if isinstance(menu, OptionsMenu):
                    self.menu_stack.remove(menu)
        else:
            self.menu_stack.append(OptionsMenu(self))
        
    def toggleInventory(self):
        if any(isinstance(menu, InventoryMenu) for menu in self.menu_stack):
            for menu in self.menu_stack:
                if isinstance(menu, InventoryMenu):
                    self.menu_stack.remove(menu)
        else:
            self.menu_stack.append(InventoryMenu(self))
        
    def toggleCharacterScreen(self):
        if any(isinstance(menu, CharacterMenu) for menu in self.menu_stack):
            for menu in self.menu_stack:
                if isinstance(menu, CharacterMenu):
                    self.menu_stack.remove(menu)
        else:
            self.menu_stack.append(CharacterMenu(self))
        
    def toggleCraftingScreen(self):
        self.craftingOpen = not self.craftingOpen
        
    def toggleChestScreen(self):
        if any(isinstance(menu, ChestMenu) for menu in self.menu_stack):
            for menu in self.menu_stack:
                if isinstance(menu, ChestMenu):
                    self.menu_stack.remove(menu)
        else:
            self.menu_stack.append(ChestMenu(self))

        
        
    def leftMouseClick(self):
        for menu in self.menu_stack[::-1]:
            if menu.startX < self.mousePos[0] < menu.endX and menu.startY < self.mousePos[1] < menu.endY:
                selectionX = menu.startX
                selectionY = math.floor((self.mousePos[1]-menu.startY)/20)
                menu.selection(selectionX, selectionY)
                return
        
        
    def updateMousePos(self, mousePos):
        self.mousePos[0] = mousePos[0] + self.viewport.x
        self.mousePos[1] = mousePos[1] + self.viewport.y
        
            
    
    #         
    # def draw_inventory(self, level):
    #     if self.inventoryOpen: #Draw own inventory
    #         startX  = self.viewport.x+(self.viewport.width-200)
    #         startY  = self.viewport.y+(self.viewport.height)-364
    #         deltaX  = 200
    #         deltaY  = 300
    #         endX    = startX+deltaX
    #         endY    = startY+deltaY
    #         
    #         pg.draw.rect(level, c.white, (startX, startY, 200,300))
    #         
    #         # Draw selection box
    #         if startX < self.mousePos[0] < endX and startY < self.mousePos[1] < endY:
    #             selectionX = startX
    #             selectionY = startY + math.floor((self.mousePos[1]-startY)/20)*20
    #             pg.draw.rect(level, c.lightblue, (selectionX, selectionY, 200, 20))
    #         
    #         if len(self.control.world.player.inventory.items):
    #             position = 0
    #             for item in self.control.world.player.inventory.items:
    #                 textObj = self.font.render(str(item.name)+'x'+str(item.amount), True, c.black)
    #                 level.blit(textObj, (self.viewport.x+(self.viewport.width-200), self.viewport.y+(self.viewport.height)+position-364))
    #                 position += 20
    #         else:                
    #             textObj = self.font.render(str('Inventory is empty' ), True, c.black)
    #             level.blit(textObj, (self.viewport.x+(self.viewport.width-200), self.viewport.y+(self.viewport.height)-364))
    #             
    #             
    #             
    #         hit = pg.sprite.spritecollide(self.control.world.player, self.control.world.object_sprites, False)
    #     
    #         if hit and isinstance(hit[0],m.Chest): #Draw chest inventory
    #             pg.draw.rect(level, c.white, (self.viewport.x+(self.viewport.width-450), self.viewport.y+(self.viewport.height)-364, 200,300))
    #             if len(hit[0].inventory.items):
    #                 position = 0
    #                 for item in hit[0].inventory.items:
    #                     textObj = self.font.render(str(item.name)+'x'+str(item.amount), True, c.black, c.white)
    #                     level.blit(textObj, (self.viewport.x+(self.viewport.width-450), self.viewport.y+(self.viewport.height)+position-364))
    #                     position += 20
                

                
    def draw_actionTiles(self,level):
        if c.options_general[1][1]:
            pg.draw.rect(level, c.white, (self.control.world.player.currentTile.rect.x, self.control.world.player.currentTile.rect.y , 64, 64))
            pg.draw.rect(level, c.red, (self.control.world.player.actionTile.rect.x, self.control.world.player.actionTile.rect.y , 64, 64))
    
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
        
        
    def update(self):
        pass
        
    def draw(self, level):
        
        self.draw_healthbars(level)
        self.draw_workbars(level)
        self.draw_hotbar(level)
        self.draw_actionTiles(level)
        for menu in self.menu_stack:
            menu.draw()
        
class Menu(object):
    def __init__(self, GUI):
        self.GUI = GUI
        self.viewport = self.GUI.viewport
        self.level = self.GUI.level

        
    def drawBackground(self):
        pg.draw.rect(self.level, c.white, (self.startX, self.startY, self.deltaX, self.deltaY))
        
    def drawSelectionBox(self):
        if self.startX < self.GUI.mousePos[0] < self.endX and self.startY < self.GUI.mousePos[1] < self.endY:
            selectionX = self.startX
            selectionY = self.startY + math.floor((self.GUI.mousePos[1]-self.startY)/20)*20
            pg.draw.rect(self.level, c.lightblue, (selectionX, selectionY, 200, 20))
        
    def drawIcons(self):
        pass
        
    def drawText(self):
        pass
    
    def update(self):
        pass
    
    def selection(self, selectX, selectY):
        pass

            
    def draw(self):
        self.update()
        self.drawBackground()
        self.drawSelectionBox()
        self.drawIcons()
        self.drawText()
        
class MainMenu(Menu):
    def __init__(self, GUI):
        super().__init__(GUI)
        self.menuOptions = c.menu_list
        self.menuHeight = len(self.menuOptions)*20
        

    def update(self):
        self.startX  = self.viewport.x+(self.viewport.width-200)
        self.startY  = self.viewport.y+(self.viewport.height)-(self.menuHeight+64)
        self.deltaX  = 200
        self.deltaY  = self.menuHeight
        self.endX    = self.startX + self.deltaX
        self.endY    = self.startY + self.deltaY
    
    def selection(self, selectX, selectY):
        selection = self.menuOptions[selectY]
        if selection == "Options":
            print('Opening options')
            self.GUI.toggleOptionsMenu()
        else:
            print(self.menuOptions[selectY])
        
    def drawText(self):
        position =0
        for item in self.menuOptions:
            textObj = self.GUI.font.render(str(item), True, c.black)
            self.level.blit(textObj, (self.startX, self.startY + position))
            position += 20

class OptionsMenu(Menu):
    def __init__(self, GUI):
        super().__init__(GUI)
        self.options = c.options_general
        
    def update(self):
        self.startX  = self.viewport.x+(self.viewport.width/2)-200
        self.startY  = self.viewport.y+(self.viewport.height/2)-100
        self.deltaX  = 400
        self.deltaY  = 200
        self.endX    = self.startX + self.deltaX
        self.endY    = self.startY + self.deltaY
        
    def drawText(self):
        position =0
        for item in self.options:
            textObj = self.GUI.font.render(str(item[0]), True, c.black)
            self.level.blit(textObj, (self.startX, self.startY + position))
            
            textObj = self.GUI.font.render(str(item[1]), True, c.black)
            self.level.blit(textObj, (self.startX + 200, self.startY + position))
            position += 20
            
    def selection(self, selectX, selectY):
        if self.options[selectY][0] == 'draw_actionTiles':
            self.options[selectY][1] = not self.options[selectY][1]
        
        
class InventoryMenu(Menu):
    def __init__(self, GUI):
        super().__init__(GUI)
        self.inventory = GUI.control.world.player.inventory
        
    def update(self):
        self.startX  = self.viewport.x+(self.viewport.width-200)
        self.startY  = self.viewport.y+(self.viewport.height)-364
        self.deltaX  = 200
        self.deltaY  = 300
        self.endX    = self.startX + self.deltaX
        self.endY    = self.startY + self.deltaY
        
    def selection(self, selectX, selectY):
        if selectY < len(self.inventory.items):
            print(self.inventory.items[selectY])
        
        
    def drawText(self):
        position = 0
        if len(self.inventory.items):
            for item in self.inventory.items:
                textObj = self.GUI.font.render(str(item.name) + 'x' + str(item.amount), True, c.black)
                self.level.blit(textObj, (self.startX, self.startY + position))
                position += 20
        else:                
            textObj = self.GUI.font.render(str('Inventory is empty' ), True, c.black)
            self.level.blit(textObj, (self.startX, self.startY + position))
            
class ChestMenu(Menu):
    def __init__(self, GUI):
        super().__init__(GUI)
        # self.inventory = 
        
    def update(self):
        self.startX  = self.viewport.x + (self.viewport.width-450)
        self.startY  = self.viewport.y + (self.viewport.height)-364
        self.deltaX  = 200
        self.deltaY  = 300
        self.endX    = self.startX + self.deltaX
        self.endY    = self.startY + self.deltaY
        
        

    # if len(self.inventory.items):
    #     position = 0
    #     for item in self.inventory.items:
    #         textObj = self.GUI.font.render(str(item.name) + 'x' + str(item.amount), True, c.black)
    #         self.level.blit(textObj, (self.startX, self.startY + position))
    #         position += 20
    # else:                
    #     textObj = self.GUI.font.render(str('Inventory is empty' ), True, c.black)
    #     self.level.blit(textObj, (self.startX, self.startY + position))
        
               
class CharacterMenu(Menu):
    def __init__(self, GUI):
        super().__init__(GUI)
        self.player = GUI.control.world.player
        self.statlist = ['healthCurrent', 'healthMax', 'manaCurrent', 'manaMax', 'movespeed', 'level', 'experience']
        
    def update(self):
        self.startX  = self.viewport.x+(self.viewport.width-200)
        self.startY  = self.viewport.y
        self.deltaX  = 200
        self.deltaY  = 400
        self.endX    = self.startX + self.deltaX
        self.endY    = self.startY + self.deltaY
    
    
    def drawText(self):
        position = 0
        for stat in self.statlist:
            textObj = self.GUI.font.render(str(stat) + ' : ' + str(self.player.__getattribute__(stat)), True, c.black)
            self.level.blit(textObj, (self.startX, self.startY + position))
            position += 20
    
        for equipment in self.player.equipped:
            textObj = self.GUI.font.render(str(equipment), True, c.black)
            self.level.blit(textObj, (self.startX, self.startY + position))
            position += 20
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        

                    
                