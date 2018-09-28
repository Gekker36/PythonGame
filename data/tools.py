import os, random
import pygame as pg
from . import constants as c
      
        
class Control(object):
    """
    Control class for entire project.  Contains the game loop, and contains
    the event_loop which passes events to States as needed.  Logic for flipping
    states is also found here.
    """
    def __init__(self, caption):
        print('Control initialized')
        self.screen = pg.display.get_surface()
        self.done = False
        # self.clock = pg.time.Clock()
        # # self.caption = caption
        # self.fps = 60
        # self.show_fps = False
        # self.current_time = 0.0
        # self.keys = pg.key.get_pressed()
        # self.state_dict = {}
        # self.state_name = None
        # self.state = None
        
    # def setup_states(self, state_dict, start_state):
    #     self.state_dict = state_dict
    #     self.state_name = start_state
    #     self.state = self.state_dict[self.state_name]
        # self.set_music()

    # def update(self):
    #     self.current_time = pg.time.get_ticks()
    #     # if self.state.quit:
    #     #     self.done = True
    #     # elif self.state.done:
    #     #     self.flip_state()
    #     self.state.update(self.screen, self.keys, self.current_time)

    # def flip_state(self):
    #     previous, self.state_name = self.state_name, self.state.next
    #     previous_music = self.state.music_title
    #     persist = self.state.cleanup()
    #     self.state = self.state_dict[self.state_name]
    #     self.state.previous = previous
    #     self.state.previous_music = previous_music
    #     self.state.startup(self.current_time, persist)
    #     self.set_music()

    # def event_loop(self):
    #     self.events = pg.event.get()

   ##       for event in self.events:
    #         if event.type == pg.QUIT:
    #             self.done = True
    #         elif event.type == pg.KEYDOWN:
    #             self.keys = pg.key.get_pressed()
    #             self.toggle_show_fps(event.key)
    #             self.state.get_event(event)
    #         elif event.type == pg.KEYUP:
    #             self.keys = pg.key.get_pressed()
    #             self.state.get_event(event)

    # def toggle_show_fps(self, key):
    #     if key == pg.K_F5:
    #         self.show_fps = not self.show_fps
    #         if not self.show_fps:
    #             pg.display.set_caption(self.caption)

    def main(self):
        """Main loop for entire program"""
        print ('Running update loop')
        while True:  #not self.done:
            # self.event_loop()
            # self.update()
            pg.display.update()
            # self.clock.tick(self.fps)
            # if self.show_fps:
            #     fps = self.clock.get_fps()
            #     with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
            #     pg.display.set_caption(with_fps)
                
                
                
class _State(object):
    """Base class for all game states"""
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.game_data = {}
        self.music = None
        self.music_title = None
        self.previous_music = None

    def get_event(self, event):
        pass

    def startup(self, current_time, game_data):
        self.game_data = game_data
        self.start_time = current_time

    def cleanup(self):
        self.done = False
        return self.game_data

    def update(self, surface, keys, current_time):
        pass            
        
def load_all_character(directory, colorkey=(255,0,255), accept=('.png', '.jpg', '.bmp')):
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            img = pg.transform.scale(img, (c.tileSize, img.get_height()*int(c.tileSize/img.get_width())))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name] = img
    return graphics
        
def load_all_gfx(directory, colorkey=(255,0,255), accept=('.png', '.jpg', '.bmp')):
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            img = pg.transform.scale(img, (c.tileSize, c.tileSize))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name] = img
    return graphics
    
def load_all_tmx(directory, colorkey=(255,0,255), accept=('.png', '.jpg', '.bmp')):
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            img = pg.transform.scale(img, (c.tileSize, c.tileSize))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name] = img
    return graphics