import pygame
from collections import defaultdict
from math import floor
from engine.buttonMenu import *

def s(t): return pygame.time.wait(floor(t * 1000))
# do not use time.sleep() - return should be useless.

class Displayer:

    def __init__(self):
        self.dict_str={} # to be changed
        pygame.init()
        self.load_images()
        self.load_options()
        self.launch_display()

    def load_images(self):
        with open("data/img/img.json", "r", encoding="utf-8-sig") as read_file:
            self.raw_img = json.load(read_file)

        dflt = pygame.image.load("data/img/default.png")
        def return_dflt(*_):
            return dflt
        self.img = defaultdict(return_dflt)

        for k,v in self.raw_img.items():
            self.img[k] = pygame.image.load("data/img/"+v)

    def load_options(self):
        with open("data/usr/options.json","r") as file:
            self.opt = json.load(file)

    def launch_display(self):
        self.test_screen()
        self.mode = 0 # mode = 0 ou FULLSCREEN
        self.win = pygame.display.set_mode((self.opt["sizex"], self.opt["sizey"]), self.mode)
        pygame.display.set_icon(self.img["R"])
        pygame.display.set_caption("Riskwizou")
        self.init_menu()

    def init_menu(self):
        self.centerx(self.img["Riskwizou"],10)
        pygame.display.flip()
        self.menu = True
        self.buttons = []
        ButtonMenu(self,"btn1",None,200,"launchgame")

    def main_menu(self):
        print("Menu")
        # self.centerx(self.img["btn1"],200)
        pygame.time.Clock().tick(24)
        keys = pygame.key.get_pressed()
        LAUNCHGAME = 0
        if keys[pygame.K_ESCAPE]:
            self.menu = False
            LAUNCHGAME = -1
        pos = pygame.mouse.get_pos()
        MOUSE = False
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                pass
            if event.type == MOUSEBUTTONDOWN:
                MOUSE = True
                LAUNCHGAME = int(xyinbounds(pos[0],pos[1],self.buttons[0]))
        self.display_buttons()
        pygame.display.flip()
        if LAUNCHGAME:
            self.menu = False
        return LAUNCHGAME

    def setmap(self,map):
        self.map = self.img["map"]

    def mouse(self):
        return pygame.mouse.get_pos()

    def keys(self):
        return pygame.key.get_pressed()

    def key_m(self):
        return self.keys()[pygame.K_m]

    def key_e(self):
        return self.keys()[pygame.K_e]

    def key_esc(self):
        return self.keys()[pygame.K_ESCAPE]

    def game(self):
        mouspos = pygame.mouse.get_pos()
        pygame.display.blit(self.map)

        self.flip()
        return mousepos

    def test_screen(self):
        """ Tests if the user's screen is large enough """
        i = pygame.display.Info()
        width = i.current_w
        height = i.current_h
        if width < self.opt["sizex"] or height < self.opt["sizey"]:
            self.opt["sizex"] = width
            self.opt["sizey"] = height
            with open("data/json/options.json","w") as f:
                f.write(json.dumps(self.opt))

    def centerx(self,surf,y=0):
        width = pygame.display.Info().current_w
        sx = surf.get_width()
        self.win.blit(surf,(width//2-sx//2,y))

    def display_buttons(self):
        for b in self.buttons:
            b.display()

    def filp(self):
        """ used in button_menu """
        pygame.display.flip()

    def set_str(self,d):
        self.dict_str = d

    def dstr(self,char):
        """ Try to find if dict_str contains a value for the key 'char'.
        If not, it  returns the char value itself.
        This function is to be used with numbers, and strings when we do not
        know at compile time whether they will be in dict_str or not."""
        try:
            return self.dict_str[char]
        except KeyError:
            return char

    def close(self):
        pygame.display.quit()
        pygame.quit()
