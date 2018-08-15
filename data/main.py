from data.states import  level #, death, shop, levels, battle,
# from data.states import credits
from . import setup, tools, inputcontroller, player
from . import constants as c
import pygame as pg
import random

tile_sprites = pg.sprite.Group()
character_sprites = pg.sprite.Group()
object_sprites = pg.sprite.Group()
spell_sprites = pg.sprite.Group()
icon_sprites = pg.sprite.Group()


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self,character_sprites)
        self.image = setup.GFX['Character']
        self.image.convert_alpha()
        self.image.set_colorkey((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 100
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False
        self.colliders=[]
        
        self.direction = 2
        self.inventory = Inventory()
        self.healthCurrent = 100
        self.healthMax = 100
        self.healthRegen = 1
        self.manaCurrent = 50
        self.manaMax = 100
        self.manaRegen = 10
        self.moveSpeed = 2
        self.level = 1
        self.experience = 0
        
        
        self.equipped = {"Head":[], "Body":[], "Weapon":[], "Shield":[]}
        self.attack = 10
        self.defence = 10
        
        
    def castFireball(self):
        print("Casting Fireball")
        Spell(self)
    
    def createChest(self):
        print("Creating Chest")
        Chest(self)
      
    def createItem(self):
        self.inventory.add_item(Item())
    
    def update(self, deltatime):
        
        self.colliders = pg.sprite.spritecollide(self, object_sprites, False)
        # if colliders:
            # print (colliders)
        
        self.currentTile=[int(round(self.rect.y-100)/64), int(round(self.rect.x/64))]
        
        if self.healthCurrent < self.healthMax:
            self.healthCurrent += self.healthRegen*deltatime
        if self.manaCurrent < self.manaMax:
            self.manaCurrent += self.manaRegen*deltatime
            
        if self.moveLeft == True:
            if self.rect.x > 0:
                self.rect.x -=self.moveSpeed
            
        if self.moveRight == True:
            if self.rect.x < (c.mapWidth-1)*64:
                self.rect.x += self.moveSpeed
               
        if self.moveUp == True:
            if self.rect.y > 100:
                self.rect.y -= self.moveSpeed
                   
        if self.moveDown == True:
            if self.rect.y < ((c.mapHeight-1)*64)+100:
                self.rect.y +=self.moveSpeed 

        
    def draw(self, screen):
        surface.blit(self.image, self.rect)

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self,character_sprites)
        self.image = setup.GFX['Enemy']
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = 64*8
        self.rect.y = (64*8)+100
        
        self.healthCurrent = 100
        self.healthMax = 100
        self.healthRegen = 1
        
    def update(self, deltatime):
        if self.healthCurrent <= 0:
            self.kill()
        
    def draw(self):
        surface.blit(self.image, self.rect)


        
class Item(object):
    def __init__(self):
        self.image = setup.GFX['Sword_icon']
        self.name = "Sword"
        self.type = "Weapon"
        self.isStackable = False
        self.price = 100
        self.amount = 1
        
        
class Inventory(object):
    def __init__(self):
        self.size = 10
        self.items=[]

        
    def add_item(self, item):
        if len(self.items)<self.size:
            self.items.append(item)
        else:
            print("Inventory is full")
            
    def remove_item(self, item):
        self.items.remove(item)
        
        
class Chest(pg.sprite.Sprite):
    def __init__(self, player):
        pg.sprite.Sprite.__init__(self,object_sprites)
        self.inventory = Inventory()
        self.image = setup.GFX["Chest Closed"]
        self.rect = self.image.get_rect()
        self.rect.x = player.currentTile[1]*64
        self.rect.y = player.currentTile[0]*64+100
        self.isOpen = False
        
        
    def update(self):
        pass
        
    def draw (self, screen):
        surface.blit(self.image, self.rect)
        
        
class Spell(pg.sprite.Sprite):
    def __init__(self, player):
        self.manaCost = 10
        if player.manaCurrent >= self.manaCost:
            pg.sprite.Sprite.__init__(self,spell_sprites)
            self.image = setup.GFX['Orb of Flame']
            self.rect = self.image.get_rect()
            self.rect.x = player.rect.x
            self.rect.y = player.rect.y
            self.image.set_colorkey((0,0,0))
            self.direction = player.direction
            self.speed = 4
            self.caster = player
            player.manaCurrent -= self.manaCost
            
    def update(self, deltatime):
        
        if self.direction == 0:
            # self.rect.x += self.speed
            self.rect.y -= self.speed
        if self.direction == 1:
            self.rect.x += self.speed
            # self.rect.y += self.speed
        if self.direction == 2:
            # self.rect.x += self.speed
            self.rect.y += self.speed
        if self.direction == 3:
            self.rect.x -= self.speed
            # self.rect.y += self.speed
            
        hit = pg.sprite.spritecollide(self, character_sprites,False)
        
        if hit:
            if hit[0] != self.caster:
                hit[0].healthCurrent -= 10
                if hit[0].healthCurrent <=0:
                    self.caster.experience +=10
                
                self.kill()
            
        if self.rect.x >= c.mapWidth*c.tileSize or self.rect.x <= -c.tileSize or self.rect.y >= c.mapHeight*c.tileSize or self.rect.y <= -c.tileSize:
            self.kill()
       
    def draw(self, screen):
        surface.blit(self.image, self.rect)
        
        

class Tile(pg.sprite.Sprite):
    def __init__(self,x,y,tileType):
        pg.sprite.Sprite.__init__(self, tile_sprites)
        self.tileType = tileType
        self.image = setup.TMX[tileType]
        self.rect = self.image.get_rect()
        self.rect.x = x*64
        self.rect.y = (y*64)+100
        self.isPassable = True

        
    def update(self):
        self.image = setup.TMX[self.tileType]
        
    def draw(self,surface):
        surface.blit(self.image, self.rect+64)

        
        
class World(object):
    def __init__(self):
        self.mapHeight = c.mapHeight
        self.mapWidth = c.mapWidth
        self.tileSize = c.tileSize
        self.worldGenerator()
        self.tilemap
        
    
    def worldGenerator(self):
        print("Create tilemap")
        self.tilemap = [[Tile(w,h,'Grass') for w in range(self.mapWidth)] for h in range(self.mapHeight)]
        
        for h in range(self.mapHeight):
            for w in range(self.mapWidth):
                if random.randint(1,100)<15 :
                    self.tilemap[h][w]= Tile(w,h,'Water')
                if random.randint(1,100)<15 :
                    self.tilemap[h][w]= Tile(w,h,'Stone')
                    
                    
class Icon(pg.sprite.Sprite):
    def __init__(self, base, inventory):
        pg.sprite.Sprite.__init__(self, icon_sprites)
        
        self.item = base
        self.image = self.item.image
        self.rect = self.image.get_rect()
        self.inventory = inventory
        
    

class GUI(object):
    def __init__(self):
        self.font = pg.font.SysFont('arial',18)
        self.playerInventory_shown = False
        self.charactersheet_shown = False
        self.mainmenu_shown = False
        self.chestInventory_shown = False

    def update_GUI(self,DISPLAYSURF, player, fpsClock):
        
        
        #Draw Top GUI
        placePosition = 10
        GUIsurface = pg.Surface((c.mapWidth*c.tileSize, 100))
        
        #Draw Health
        textObj = self.font.render(str('HEALTH: ') +str(int(player.healthCurrent)) + str(' / ') + str(int(player.healthMax)), True, c.white, c.black)
        GUIsurface.blit(textObj, (placePosition, 5))
        #Draw Mana
        textObj = self.font.render(str('MANA: ') +str(int(player.manaCurrent)) + str(' / ') + str(int(player.manaMax)), True, c.white, c.black)
        GUIsurface.blit(textObj, (placePosition, 25))
        #Draw level
        textObj = self.font.render(str('Level: ') +str(int(player.level)), True, c.white, c.black)
        GUIsurface.blit(textObj, (placePosition, 45))
        #Draw Experience
        textObj = self.font.render(str('Experience: ') +str(int(player.experience)) , True, c.white, c.black)
        GUIsurface.blit(textObj, (placePosition, 65))
        
        placePosition += 150
        #Print FPS
        textObj = self.font.render(str(fpsClock), True, c.white, c.black)
        GUIsurface.blit(textObj, (placePosition, 5))
        
        #Print number of spell Sprites
        textObj = self.font.render(str(len(spell_sprites)), True, c.white, c.black)
        GUIsurface.blit(textObj, (placePosition, 25))
        
        #Print number of icon Sprites
        textObj = self.font.render(str(len(icon_sprites)), True, c.white, c.black)
        GUIsurface.blit(textObj, (placePosition, 45))
        
        DISPLAYSURF.blit(GUIsurface,(0,0))
        
        icon_sprites.empty()
        #Draw inventory screen
        if self.playerInventory_shown:
            #Draw own inventory
            placepositionx = 0
            placepositiony = 0
            
            playerInventorySurface = pg.Surface((128,320))
            playerInventorySurface.fill(c.white)
            
            #Draw player inventory  
            #Draw empty spots
            for i in range(player.inventory.size):
                playerInventorySurface.blit(setup.GFX["Empty Inventory"], (placepositionx,placepositiony))
                placepositiony += 64
                if placepositiony >= 320:
                    placepositiony = 0
                    placepositionx += 64
                    
                    
            #Draw filled spots      
            placepositionx = 0
            placepositiony = 0
            for item in player.inventory.items:
                icon=Icon(item, player.inventory)
                playerInventorySurface.blit(icon.image, (placepositionx,placepositiony))
                icon.rect.x = placepositionx+512
                icon.rect.y = placepositiony+100
                placepositiony += 64
                if placepositiony >= 320:
                    placepositiony = 0
                    placepositionx += 64
            DISPLAYSURF.blit(playerInventorySurface,(512,100))
            
            
            #Draw chest inventory 
            

            if len(player.colliders)>=1:
                
                chestInventorySurface = pg.Surface((128,320))
                chestInventorySurface.fill(c.white)
                placepositionx = 0
                placepositiony = 0
                    
                for i in range(player.inventory.size):
                    chestInventorySurface.blit(setup.GFX["Empty Inventory"], (placepositionx,placepositiony))
                    placepositiony += 64
                    if placepositiony >= 320:
                        placepositiony = 0
                        placepositionx += 64
                        
                        
                placepositionx = 0
                placepositiony = 0
                for item in player.colliders[0].inventory.items:
                    icon=Icon(item, player.colliders[0].inventory)
                    chestInventorySurface.blit(icon.image, (placepositionx,placepositiony))
                    icon.rect.x = placepositionx+320
                    icon.rect.y = placepositiony+100
                    placepositiony += 64
                    if placepositiony >= 320:
                        placepositiony = 0
                        placepositionx += 64
                DISPLAYSURF.blit(chestInventorySurface,(320,100))
                

        #Draw CharacterSheet screen
        if self.charactersheet_shown:

            placepositionx = 0
            placepositiony = 0
            
            characterSheetSurface = pg.Surface((124,400))
            characterSheetSurface.fill(c.white)
            
            for key in player.equipped:
                textObj = self.font.render(str(key), True, c.white, c.black)
                characterSheetSurface.blit(textObj, (placepositionx, placepositiony))
                placepositiony +=20
                
                if player.equipped[key]:
                    icon=Icon(player.equipped[key], player.equipped)
                    icon.rect.x = placepositionx
                    icon.rect.y = placepositiony+100
                    characterSheetSurface.blit(icon.image, (placepositionx, placepositiony))
                    
                else:
                    characterSheetSurface.blit(setup.GFX["Empty Inventory"], (placepositionx, placepositiony))
                
            
                placepositiony +=80
            
            DISPLAYSURF.blit(characterSheetSurface,(0,100))
        
        #Draw MainMenu
        if self.mainmenu_shown:
            square = pg.draw.rect(DISPLAYSURF,c.white,(400,100,250,300))

class GameControl(object):
    def __init__(self):
        self.screen = setup.SCREEN
        self.screen_rect = setup.SCREEN_RECT
        self.clock = pg.time.Clock()
        self.quit = False
        
        
        
    def update_events(self):
        inputcontroller.playerInput(self)
        tile_sprites.update()
        spell_sprites.update(self.deltatime)
        character_sprites.update(self.deltatime)
        
        
    def update_screen(self):
        tile_sprites.draw(self.screen)
        spell_sprites.draw(self.screen)
        object_sprites.draw(self.screen)
        character_sprites.draw(self.screen)
        self.gui.update_GUI(self.screen,self.player,self.fpsClock)
        
        
    def main(self):
        print("GameControl init")
        
        # print("Create sprite group")
        # sprites = pg.sprite.Group()
        
        print("Create world")
        self.world = World()
        
        print("Create player")
        self.player = Player()
        
        print("Create GUI")
        self.gui = GUI()
        
        print("Starting main loop")
        while not self.quit:
            self.deltatime = self.clock.tick()/1000
            self.fpsClock = self.clock.get_fps()
            
            #Update game events
            self.update_events()
            
            #Draw game sprites
            self.update_screen()
            
            pg.display.update()
        
        
        

def main():
    
    print("Create GameControl")
    gameControl = GameControl().main()
    

    
   
    
    
    