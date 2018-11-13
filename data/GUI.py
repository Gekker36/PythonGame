import pygame as pg
import math
from . import constants as c
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


    # def selectMainMenu(self):
    #     if not self.menuOpen:
    #         self.menuOpen = True
    #         self.menu_stack.append('main')
    #         print (self.menu_stack)
    #         
    #     
    # def returnMainMenu(self):
    #     if self.menu_stack[-1] == 'main':
    #         self.menuOpen = False
    #         self.menu_stack.remove('main')
    #          
    # 
    def menu_selecting(self, change):
        self.mainMenuSelection+= change
        if self.mainMenuSelection < 0:
            self.mainMenuSelection = len(c.menu_options)-1
        if self.mainMenuSelection > len(c.menu_options)-1:
            self.mainMenuSelection = 0
            
    def openMainMenu(self):
        
        if any(isinstance(menu, Menu) for menu in self.menu_stack):
            for menu in self.menu_stack:
                if isinstance(menu, MainMenu):
                    self.menu_stack.remove(menu)
                    print('Closing mainmenu')
        
        else:
            self.menu_stack.append(MainMenu(self))
            print('Opening mainmenu')
        
        
    def openInventory(self):
        self.inventoryOpen = not self.inventoryOpen
        
    def openCharacterScreen(self):
        self.charactersheetOpen = not self.charactersheetOpen
        
    def openCraftingScreen(self):
        self.craftingOpen = not self.craftingOpen
        
    def updateMousePos(self, mousePos):
        self.mousePos[0] = mousePos[0] + self.viewport.x
        self.mousePos[1] = mousePos[1] + self.viewport.y
        # print(self.mousePos)
        
            
    def draw_mainMenu(self, level):
        if self.mainMenuOpen:
            
            menuHeight = len(c.menu_options)*20
            startX  = self.viewport.x+(self.viewport.width-200)
            startY  = self.viewport.y+(self.viewport.height)-(menuHeight+64)
            deltaX  = 200
            deltaY  = menuHeight
            endX    = startX+deltaX
            endY    = startY+deltaY
            
            pg.draw.rect(level, c.white, (startX, startY, deltaX, deltaY))
            
            # Draw selection box
            if startX < self.mousePos[0] < endX and startY < self.mousePos[1] < endY:
                selectionX = startX
                selectionY = startY + math.floor((self.mousePos[1]-startY)/20)*20
                pg.draw.rect(level, c.lightblue, (selectionX, selectionY, 200, 20))
                
            position =0
            for item in c.menu_options:
                textObj = self.font.render(str(item), True, c.black)
                level.blit(textObj, (self.viewport.x+(self.viewport.width-200), self.viewport.y+(self.viewport.height)+position-(menuHeight+64)))
                position += 20
            
    def draw_inventory(self, level):
        if self.inventoryOpen: #Draw own inventory
            startX  = self.viewport.x+(self.viewport.width-200)
            startY  = self.viewport.y+(self.viewport.height)-364
            deltaX  = 200
            deltaY  = 300
            endX    = startX+deltaX
            endY    = startY+deltaY
            
            pg.draw.rect(level, c.white, (startX, startY, 200,300))
            
            # Draw selection box
            if startX < self.mousePos[0] < endX and startY < self.mousePos[1] < endY:
                selectionX = startX
                selectionY = startY + math.floor((self.mousePos[1]-startY)/20)*20
                pg.draw.rect(level, c.lightblue, (selectionX, selectionY, 200, 20))
            
            if len(self.control.world.player.inventory.items):
                position = 0
                for item in self.control.world.player.inventory.items:
                    textObj = self.font.render(str(item.name)+'x'+str(item.amount), True, c.black)
                    level.blit(textObj, (self.viewport.x+(self.viewport.width-200), self.viewport.y+(self.viewport.height)+position-364))
                    position += 20
            else:                
                textObj = self.font.render(str('Inventory is empty' ), True, c.black)
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
                
    def draw_actionTiles(self,level):
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
        for menu in self.menu_stack:
            menu.draw()
        self.draw_healthbars(level)
        self.draw_workbars(level)
        self.draw_hotbar(level)
        self.draw_mainMenu(level)
        self.draw_inventory(level)
        self.draw_charactersheet(level)
        self.draw_actionTiles(level)
        
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
        position =0
        for item in c.menu_options:
            textObj = self.GUI.font.render(str(item), True, c.black)
            self.level.blit(textObj, (self.viewport.x+(self.viewport.width-200), self.viewport.y+(self.viewport.height)+position-(self.menuHeight+64)))
            position += 20
            
    def draw(self):
        self.drawBackground()
        self.drawSelectionBox()
        self.drawIcons()
        self.drawText()
        
class MainMenu(Menu):
    def __init__(self, GUI):
        super().__init__(GUI)
        self.menuHeight = len(c.menu_options)*20
        self.startX  = self.viewport.x+(self.viewport.width-200)
        self.startY  = self.viewport.y+(self.viewport.height)-(self.menuHeight+64)
        self.deltaX  = 200
        self.deltaY  = self.menuHeight
        self.endX    = self.startX + self.deltaX
        self.endY    = self.startY + self.deltaY
        
class InventoryMenu(Menu):
    def __init__(self, GUI):
        super().__init__(GUI)
        self.startX  = self.viewport.x+(self.viewport.width-200)
        self.startY  = self.viewport.y+(self.viewport.height)-364
        self.deltaX  = 200
        self.deltaY  = 300
        self.endX    = self.startX + self.deltaX
        self.endY    = self.startY + self.deltaY
        
class CharacterMenu(Menu):
    def __init__(self, GUI):
        super().__init__(GUI)
        self.startX  = self.viewport.x+(self.viewport.width-200)
        self.startY  = self.viewport.y+(self.viewport.height)-364
        self.deltaX  = 200
        self.deltaY  = 300
        self.endX    = self.startX + self.deltaX
        self.endY    = self.startY + self.deltaY
        
        

                    
                