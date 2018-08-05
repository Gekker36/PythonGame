import sys
import pygame as pg
from data import setup
from data.main import main


if __name__ =='__main__':
    setup.GAME
    main()
    pg.quit()
    # sys.exit()