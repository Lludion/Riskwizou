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
        self.pygame = pygame
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
        self.win.blit(self.img["bg"],(0,0))
        self.centerx(self.img["Riskwizou"],10)
        pygame.display.flip()
        self.menu = True
        self.buttons = []
        ButtonMenu(self,"btn1",None,200,"launchgame")

    def main_menu(self):
        print("Menu")
        # self.centerx(self.img["btn1"],200)
        self.tick()
        keys = pygame.key.get_pressed()
        LAUNCHGAME = 0
        pos = pygame.mouse.get_pos()
        MOUSE = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.menu = False
                    LAUNCHGAME = -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                MOUSE = True
                LAUNCHGAME = int(xyinbounds(pos[0],pos[1],self.buttons[0]))
        self.display_menu()
        if LAUNCHGAME:
            self.menu = False
        return LAUNCHGAME

    def setmap(self,map):
        self.map = self.img[map]
        w = self.win.get_width()
        h = self.win.get_height()
        if w/h >= 4000/2640:
            self.map = pygame.transform.scale(self.map, (4000*h//2640,h))
            self.mapx = 4000*h//2640
            self.mapy = h
        else:
            self.map = pygame.transform.scale(self.map, (w,2640*w//4000))
            self.mapx = w
            self.mapy = 2640*w//4000

        # changing the size of boxes
        self.boxl = self.mapy //3
        self.img["box"] = pygame.transform.scale(self.img["box"], (self.boxl,self.boxl))

    def mouse(self):
        return pygame.mouse.get_pos()

    def keys(self):
        return pygame.key.get_pressed()

    def k_events(self):
        return [event for event in pygame.event.get() if event.type == pygame.KEYDOWN]

    def flclic(self):
        """ flushes the received events and checks for a mousebuttonsdown"""
        return [event for event in pygame.event.get() if event.type == pygame.MOUSEBUTTONDOWN]

    def clic(self,btn = 0):
        return pygame.mouse.get_pressed()[btn]

    def key_m(self):
        """ true if m is down """
        return self.keys()[pygame.K_m]

    def game(self):
        self.tick()
        self.flip()
        self.win.blit(self.map,(0,0))
        mousepos = pygame.mouse.get_pos()
        return self.correctmouse(mousepos)

    def correctmouse(self,mouse):
        return mouse[0]*4000//self.mapx,mouse[1]*2640//self.mapy

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

    def flip(self):
        """ used in button_menu """
        pygame.display.flip()

    def tick(self,t=None):
        """ used in loops """
        if t is None: t  = self.opt["FPS"]
        pygame.time.Clock().tick(t)

    def centerx(self,surf,y=0):
        width = pygame.display.Info().current_w
        sx = surf.get_width()
        self.win.blit(surf,(width//2-sx//2,y))

    def display_buttons(self):
        for b in self.buttons:
            b.display()

    def display_menu(self):
        self.win.blit(self.img["bg"],(0,0))
        self.centerx(self.img["Riskwizou"],10)
        self.display_buttons()
        self.flip()

    def zonebox(self,z):
        h = self.win.get_height()
        fw = self.img["box"].get_width()
        fh = h - self.img["box"].get_height()
        self.win.blit(self.img["box"], (0,fh))
        T(self.win,self.dstr(z.name),20,fh+5,255,255,255,center=False,size=25)
        if z.troops:
            own = z.troops[0].owner
            if own is None:
                c1 = c2 = c3 = 125
                ownname = self.dstr("independent")
            else:
                c1 = own.color[0]
                c2 = own.color[1]
                c3 = own.color[2]
                ownname = self.dstr(own.name)
            for i in range(len(self.g.dut)):
                u = self.g.dut[i]
                T(self.win,self.dstr(u().name)+" : "+str(len([x for x in z.troops if x.name == u().name])),24,fh+30+28*i,c1,c2,c3,center=False,size=30)
            T(self.win,ownname,fw-2-len(ownname)*8,fh+10,c1,c2,c3,center=False)
        else:
            T(self.win,self.dstr("independent"),fw-2-len(self.dstr("independent"))*8,fh+10,255,200,200,center=False)

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
