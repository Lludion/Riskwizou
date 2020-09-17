import pygame
import random
from pygame.locals import *
from tools.xyinbounds import xyinbounds
from tools.text_display import T
from shutil import copy2
import json
from os import listdir
from os import getcwd

"""Reaction functions of the buttons

input   : a Displayer      :
returns : bool x bool :  cnt,quit_all such that:
                        cnt : do we continue the current loop?
                        quit_all : do we quit all loops ?
"""

def no_reaction(g):
    """ the most trivial reaction of a button. It has no effect."""
    return True, False

def reaction_exit(g):#quitte le jeu
    """ exits the game """
    return False,True

class ButtonMenu:

    def __init__(self,g,img,xm,ym,text=None,name="Unnamed",picH=None,picD=None,react=no_reaction,add_to_list=True,colour=None):
        self.g = g#the displayer where the buttons will be displayed

        if xm is None:
            xm = pygame.display.Info().current_w//2-self.g.img[img].get_width()//2
        self.xmin = xm
        self.ymin = ym
        self.xmax = xm + self.g.img[img].get_width()
        self.ymax = ym + self.g.img[img].get_height()
        self.pic = self.g.img[img]
        self.activated = True
        if picH is None: self.picH = self.g.img[img+"H"]
        else: self.picH = self.g.img[picH] #hovering
        if picD is None: self.picD = self.g.img[img+"D"]
        else: self.picD = self.g.img[picD]#deactivated
        self.picHD = self.g.img[img+"HD"]
        if text is None: self.text = ""
        else: self.text = text#displayed text
        self.t = 0
        self.up = True
        if add_to_list:
            g.buttons.append(self)#to keep an eye on all buttons
        self.name = name
        self.speed = 1
        self.period = 1
        self.react = react
        self.visible = True
        self.was_active = True#manages activation ~ disappearance relations
        self.offsetX = 0
        self.colour = colour

    def __repr__(self):
        return self.name + '= Button(%s<x<%s, %s<y<%s)\n' % (self.xmin, self.xmax, self.ymin, self.ymax)

    def __displayedY(self,yy):
        return yy - self.period//2 + ((self.t//self.speed)%self.period)

    def set_offset(self,offset):
        """ sets the offset of the text """
        self.offsetX = offset

    def boundaries(self):
        """ returns the visible boundaries of self"""
        return self.xmin,self.xmax,self.__displayedY(self.ymin),self.__displayedY(self.ymax)

    def activation(self,flag):
        self.activated = flag
        self.was_active = flag
        return self

    def appear(self):
        """ an invisible button appears"""
        self.visible = True
        self.activated = self.was_active

    def disappear(self):
        """ a button disappears """
        self.visible = False
        self.was_active = self.activated
        self.activated = False

    def display(self,period=None,speed=None,refresh=False,lock=False):
        """allow for the display of buttons"""
        if self.visible:
            mx,my = pygame.mouse.get_pos()
            if self.activated:
                if xyinbounds(mx,my,self):
                    picture = self.picH
                else:
                    picture = self.pic
            else:
                if xyinbounds(mx,my,self):
                    picture = self.picHD
                else:
                    picture = self.picD
            if speed is None: speed = self.speed
            else: self.speed = speed
            if period is None: period = self.period
            else: self.period = period
            if period <= 1: self.g.win.blit(picture,(self.xmin-self.offsetX,self.ymin))
            else:
                if self.up:self.t += 1
                else: self.t -= 1
                if self.t >= period - 1:
                    self.up = False
                elif self.t <= 0:
                    self.up = True
                self.g.win.blit(picture,(self.xmin-self.offsetX,self.__displayedY(self.ymin)))
            if self.colour is None:
                if self.activated:
                    T(self.g.win,self.g.dstr(self.text),(self.xmin+self.xmax)/2,(self.__displayedY(self.ymin)+self.__displayedY(self.ymax))/2,size=50)
                else:
                    T(self.g.win,self.g.dstr(self.text),(self.xmin+self.xmax)/2,(self.__displayedY(self.ymin)+self.__displayedY(self.ymax))/2,50,50,50,size=50)
                    if lock: self.g.win.blit(self.g.dict_img["img_layer_lock"],(self.xmin-self.offsetX,self.__displayedY(self.ymin)))
            else:
                T(self.g.win.self.g.dstr(self.text),(self.xmin+self.xmax)/2,(self.__displayedY(self.ymin)+self.__displayedY(self.ymax))/2,self.colour[0],self.colour[1],self.colour[2],size=50)

            if refresh: g.flip()
