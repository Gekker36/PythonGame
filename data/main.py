from data.states import  level #, death, shop, levels, battle,
# from data.states import credits
from . import setup, tools, inputcontroller, player
from . import constants as c
import pygame as pg
import random




class Player(object):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = setup.GFX['Character']
        self.image.convert_alpha()
        self.image.set_colorkey((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.x = 0
        self.y = 0
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False
        
        self.direction = 2
        self.inventory = {'Grass': 0, 'Water': 0, 'Stone': 0}
        self.healthCurrent = 100
        self.healthMax = 100
        self.healthRegen = 1
        self.manaCurrent = 50
        self.manaMax = 100
        self.manaRegen = 1
        self.moveSpeed = 2
        
    def castFireball(self):
        print("Casting Fireball")
        Spell(self)
        
    
    def updatePlayer(self, DISPLAYSURF, deltatime):
        
        if self.healthCurrent < self.healthMax:
            self.healthCurrent += (self.healthRegen*deltatime)
        if self.manaCurrent < self.manaMax:
            self.manaCurrent += (self.manaRegen*deltatime)  
            
        if self.moveLeft == True:
            if self.x >= 0:
                self.x -=self.moveSpeed*deltatime
            
        if self.moveRight == True:
            if self.x <= c.mapWidth-1:
                self.x += self.moveSpeed*deltatime
               
        if self.moveUp == True:
            if self.y>= 0:
                self.y -= self.moveSpeed*deltatime
                   
        if self.moveDown == True:
            if self.y <= c.mapHeight-1:
                self.y +=self.moveSpeed*deltatime 
            
        DISPLAYSURF.blit(self.image, (self.x*c.tileSize,self.y*c.tileSize+100))
        
class Spell(object):
    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        self.image = setup.GFX['Orb of Flame']
        self.rect = self.image.get_rect()
        self.screen = pg.display.get_surface()
        self.castSpell(player)
        
    def castSpell(self, player):
        self.manaCost = 10
        self.direction = player.direction
        self.speed = 4
        self.x = player.x
        self.y = player.y
        surface = pg.Surface(self.rect.size)
        surface.set_colorkey(c.black)
        surface.blit(self.image, self.rect)

        
    def updateSpell(self, deltatime):
        self.x +=self.speed*deltatime
        surface = pg.Surface(self.rect.size)
        surface.set_colorkey(c.black)
        surface.blit(self.image, self.rect)
        
        

class Tile(object):
    def __init__(self,x,y,tileType):
        pg.sprite.Sprite.__init__(self)
        self.tileType = tileType
        self.image = setup.TMX[tileType]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        self.image = setup.TMX[self.tileType]
        
    def draw(self,surface):
        surface.blit(self.image, self.rect)
        
        
class World(object):
    def __init__(self):
        self.mapHeight = c.mapHeight
        self.mapWidth = c.mapWidth
        self.worldGenerator()
        self.tilemap
        self.gameObjects = pg.sprite.Group()
    
    def worldGenerator(self):
        print("Create tilemap")
        self.tilemap = [[Tile(w,h,'Grass') for w in range(self.mapWidth)] for h in range(self.mapHeight)]
        
        for h in range(self.mapHeight):
            for w in range(self.mapWidth):
                if random.randint(1,100)<15 :
                    self.tilemap[h][w]= Tile(w,h,'Water')
                if random.randint(1,100)<15 :
                    self.tilemap[h][w]= Tile(w,h,'Stone')

class GUI(object):
    def __init__(self):
        self.font = pg.font.SysFont('arial',18)

    def update_GUI(self,DISPLAYSURF, player, fpsClock):
        placePosition = 10
        
        GUIsurface = pg.Surface((c.mapWidth*c.tileSize, 100))
        
        #Draw Health
        textObj = self.font.render(str('HEALTH: ') +str(int(player.healthCurrent)) + str(' / ') + str(int(player.healthMax)), True, c.white, c.black)
        GUIsurface.blit(textObj, (placePosition, 5))
        #Draw Mana
        textObj = self.font.render(str('MANA: ') +str(int(player.manaCurrent)) + str(' / ') + str(int(player.manaMax)), True, c.white, c.black)
        GUIsurface.blit(textObj, (placePosition, 40))
        placePosition += 150
        
        #Draw resources
        for item in player.inventory:
            image = setup.TMX[item]
        
            textObj = self.font.render(str(player.inventory[item]), True, c.white, c.black)
            GUIsurface.blit(image, (placePosition,5))
            GUIsurface.blit(textObj, (placePosition,5))
            placePosition +=70
            
            
        textObj = self.font.render(str(fpsClock), True, c.white, c.black)
        GUIsurface.blit(textObj, (placePosition, 5))
        DISPLAYSURF.blit(GUIsurface,(0,0))

    def make_dialogue_box(self):
        image = setup.TMX['Stone']
        rect = image.get_rect()
        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.black)
        surface.blit(image, rect)
        surface.blit(image, rect)
        dialogue = self.font.render("Schrijf hier text",
                                    True,
                                    c.black)
        dialogue_rect = dialogue.get_rect(left=50, top=50)
        surface.blit(dialogue, dialogue_rect)
        sprite = pg.sprite.Sprite()
        sprite.image = surface
        sprite.rect = rect
        return sprite
        

class GameControl(object):
    def __init__(self):
        self.screen = pg.display.set_mode((c.mapWidth*c.tileSize, c.mapHeight*c.tileSize+100))
        self.clock = pg.time.Clock()
        self.quit = False
        
        
    def update_events(self):
        inputcontroller.playerInput(self)
        
        
        
    def update_screen(self):
        for row in range(c.mapHeight):
            for column in range(c.mapWidth):
                self.screen.blit(self.world.tilemap[row][column].image,(column*c.tileSize,row*c.tileSize+100))
                
        
        self.player.updatePlayer(self.screen,self.deltatime)
        self.gui.update_GUI(self.screen,self.player,self.fpsClock)
        
        
    def main(self):
        print("GameControl init")
        
        print("Create world")
        self.world = World()
        
        print("Create player")
        self.player = Player()
        
        print("Create GUI")
        self.gui = GUI()
        
        while not self.quit:
            self.deltatime = self.clock.tick()/1000
            self.fpsClock = self.clock.get_fps()
            self.update_events()
            self.update_screen()
            pg.display.update()
        
        
        

def main():
    
    print("Create GameControl")
    gameControl = GameControl().main()
    

    
   
    
    
    