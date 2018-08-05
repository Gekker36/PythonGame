import pygame as pg
import random
from . import constants as c
from . import main as m


def worldGenerator():
    tilemap= [[m.Tile(w,h,0) for w in range(c.mapWidth)] for h in range(c.mapHeight)]
    
    # for h in range(c.mapHeight):
    #     for w in range(c.mapWidth):
    #         if random.randint(1,100)<15 :
    #             tilemap[h][w]= m.Tile(w,h,1)
    #         if random.randint(1,100)<15 :
    #             tilemap[h][w]= m.Tile(w,h,0)
        
    

    return tilemap