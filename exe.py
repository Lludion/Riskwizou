from abstract import DGame,Game,Networker
from engine.display import Displayer
from earth import earth,players
from tools.text_display import T
from units import default_unit_types
import json

class Almighty:

    def __init__(self):
        """ Initialization """
        self.language = "french"
        with open("data/lang/"+self.language+".json", "r", encoding="utf-8-sig") as read_file:
            self.dict_str = json.load(read_file)
        self.d = Displayer()
        self.d.set_str(self.dict_str)

    def menu(self):
        menureturn = 0
        while menureturn >= 0:
            while self.d.menu:
                menureturn = self.d.main_menu()
            if menureturn == 1:
                self.launch_game()
                self.d.menu = True
        self.delgdpipe()
        self.d.close()
        del self.d

    def setgdpipe(self):
        """ sets a mean of communication between the game and the displayer """
        self.g.d = self.d
        self.d.g = self.g

    def delgdpipe(self):
        """ deletes a mean of communication between the game and the displayer """
        try:
            del self.g.d
            del self.d.g
        except AttributeError:
            pass

    def launch_game(self):
        self.begin_game()
        self.play_game()

    def pf(self,k,*args,**kwargs):
        T(self.d.win,str(k),0,0+self.toffset,200,200,200,center=False)# temporary, will be improved
        # with offsets described in self.toffset, and a nice buffer and background
        self.toffset+=20
        self.d.flip()

    def begin_game(self,w=earth,p=players,dut=default_unit_types):
        self.toffset = 0
        self.g = DGame(self.pf,w)
        self.setgdpipe() # now that the game is created
        self.g.set_p(p)
        self.g.dut = dut
        self.g.dstr = self.dstr
        self.g.begin()

    def play_game(self):
        while not self.g.ended:
            self.g.turn()

    def dstr(self,char):
        """ Try to find if dict_str contains a value for the key 'char'.
        If not, it  returns the char value itself.
        This function is to be used with numbers, and strings when we do not
        know at compile time whether they will be in dict_str or not."""
        try:
            return self.dict_str[char]
        except KeyError:
            return char
