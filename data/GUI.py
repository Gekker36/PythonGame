import pygame as pg
from . import constants as c
from . import main as m
from . import setup


# class Hotbar(object):
#     def init(self)

def draw_healthbars(screen):
    for enemy in m.character_sprites:
        if enemy.healthCurrent < enemy.healthMax:
            length = 64*(enemy.healthCurrent/enemy.healthMax)
            pg.draw.rect(screen, c.red, (enemy.rect.x,enemy.rect.y-15,length,10))
        
def draw_workbars(screen):
    for resource in m.resource_sprites:
        if resource.jobTimer !=0:
            length = 64*(resource.jobTimer/resource.jobTime)
            pg.draw.rect(screen, c.blue, (resource.rect.x,resource.rect.y-15,length,10))

def draw_hotbar(screen):
    pg.display.get_surface().blit(setup.GFX['Empty_Inventory'].convert(), (100,100))
    
def update():
    pass
    
def draw(screen):
    draw_healthbars(screen)
    draw_workbars(screen)
    draw_hotbar(screen)
                
                
    # print('test')