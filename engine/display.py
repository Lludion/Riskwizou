import pygame
from collections import defaultdict
from math import floor
from engine.buttonMenu import *
from tools import selection
from tools.list import fullpm
from tools.misc import colorname
from random import choice

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
        self.printedunits = []
        self.selectedunits = []

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
        """" POWERFUl FUNCTION """
        return [event for event in pygame.event.get() if event.type == pygame.KEYDOWN]

    def flclic(self):
        """" POWERFUl FUNCTION
         flushes the received events and checks for a mousebuttonsdown"""
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
        self.classicbox()
        self.owncircles()
        mousepos = pygame.mouse.get_pos()
        return self.correctmouse(mousepos)

    def czc(self,z):
        """ correct zone center of a zone
        (knowing the real size of the map on screen)"""
        return self.incorrectmouse(z.center())

    def owncircles(self):
        """ draws circles on provinces according to their owner """
        for c in self.g.w.continents:
            for z in c.zones:
                if z.owner is not None:
                    pygame.draw.circle(self.win,z.owner.color,self.czc(z),10)
                    if z.owner.capital is z:
                        self.win.blit(pygame.transform.scale(self.img["star"], (10,10)), self.czc(z))

    def correctmouse(self,mouse):
        return mouse[0]*4000//self.mapx,mouse[1]*2640//self.mapy

    def incorrectmouse(self,mouse):
        return mouse[0]*self.mapx//4000,mouse[1]*self.mapy//2640

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

    def display_box(self):
        h = self.win.get_height()
        fw = self.img["box"].get_width()
        fh = h - self.img["box"].get_height()
        self.win.blit(self.img["box"], (0,fh))
        return fw,fh

    def classicbox(self):
        fw,fh =  self.display_box()
        T(self.win,self.dstr(self.player_otm.name),20,fh+5,0,0,0,center = False,size=25)

    def print_unit_i(self,i,z,c1,c2,c3,ownname,fh):
        """ prints all the units of the type dut[i],
        regrouping them by remaining pm """
        u = self.g.dut[i]

        if fullpm(u,z):#if exists a full pm unit:
            a1,a2,a3,a4 = T(self.win,self.dstr(u().name)+" : "+str(len(fullpm(u,z))),24,fh+30+28*i,c1,c2,c3,center=False,size=30)

            # try to print no unit twice
            TRIES = 0
            tau = fullpm(u,z)[TRIES]
            while tau in [x for (_,_,_,_,x) in self.printedunits] and TRIES < z.ntroops():
                TRIES += 1
                tau = fullpm(u,z)[TRIES % len(fullpm(u,z))]
            if TRIES >= z.ntroops():
                print("already printed !")
            else:
                self.printedunits.append((a1,a2,a3,a4,tau))

        for x in z.troops:
            if x.pm != x.pmmax and x.name == u().name:
                a1,a2,a3,a4 = T(self.win,self.dstr(u().name) + " " + str(x.pm) + "/" + str(x.pmmax)  + " : "+str(len([y for y in z.troops if y.name == x.name and y.pm == x.pm])),24,fh+30+28*i,c1,c2,c3,center=False,size=30)
                self.printedunits.append((a1,a2,a3,a4,x))

    def zonebox(self,z=None):
        if z is None:
            self.classicbox()
        else:
            fw,fh = self.display_box()
            if z.troops:
                c1,c2,c3,ownname = colorname(self.dstr,z.troops[0].owner)

                self.printedunits = []
                for i in range(len(self.g.dut)):
                    self.print_unit_i(i,z,c1,c2,c3,ownname,fh)
                if self.selectedunits:
                    T(self.win,str(len(self.selectedunits)) + self.dstr("selected"),24,fh+30+28*len(self.g.dut),c1,c2,c3,center=False,size=30)
            else:
                c1 = c2 = c3 = 65
                ownname = self.dstr("independent")
                T(self.win,self.dstr("notroops"),24,fh+30,c1,c2,c3,center=False,size=30)

            # printing top of the box
            _,x,_,_ = T(self.win,self.dstr(z.name),20,fh+5,205,205,205,center=False,size=25)
            _,x,_,_ = T(self.win," - ",x,fh+5,205,205,205,center=False,size=25)
            _,x,_,_ = T(self.win,ownname,x,fh+5,c1,c2,c3,center=False,size=25)
            if z.owner:
                if z.owner.capital is z:
                    self.win.blit(pygame.transform.scale(self.img["star"],(40,40)), (x , fh - 15))

    def clicked_on_unit(self,z):
        """" POWERFUl FUNCTION

         used when clicking on units to select them """
        if [x for x in z.troops if x.owner == self.g.playingnow]: # nodiplomacy
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx,my = pygame.mouse.get_pos()
                    for (xm,xM,ym,yM,u) in self.printedunits:
                        if selection.box(xm,mx,xM,ym,my,yM):
                            print("Unit selected.")
                            self.selectedunits.append(u)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        if self.selectedunits: # units have been selected
                            print("All units selected!")
                            return 2
                        else:
                            return -1
                    if event.key == pygame.K_q:
                        print("quit!")
                        return -1
            return 1
        else: # no units are selectable
            return -1

    def select_units(self,z,maxn=2,minn=2):
        """" POWERFUl FUNCTION """
        if z.troops: # nodiplomacy
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx,my = pygame.mouse.get_pos()
                    for (xm,xM,ym,yM,u) in self.printedunits:
                        if selection.box(xm,mx,xM,ym,my,yM):
                            if len(self.selectedunits) < maxn:
                                self.selectedunits.append(u)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        if self.selectedunits and len(self.selectedunits) >= minn: # units have been selected
                            print("small number selected")
                            return 2
            if len(self.selectedunits) == maxn:
                return 2
            else:
                return 1
        else: # no units are selectable
            return -1


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
