import os
import pygame as pg
from . import tools
from . import constants as c


GAME = 'BEGIN GAME'

ORIGINAL_CAPTION = 'My first Pygame'

os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()
pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode((800, 800))
SCREEN_RECT = SCREEN.get_rect()



CFX = tools.load_all_character(os.path.join('resources','graphics', 'characters', 'player' ))
GFX = tools.load_all_gfx(os.path.join('resources', 'graphics', 'default'))
TMX = tools.load_all_tmx(os.path.join('resources','graphics', 'tiles'))





