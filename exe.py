from abstract import DGame,Game,Networker
from engine.display import Displayer
from earth import earth,create_earth,players
from tools.text_display import T
from net.networking import NetworkClient,NetworkServer,masterip
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
        self.player_otm = None # on this machine
        self.toffset = 0

    def menu(self):
        menureturn = 0
        while menureturn >= 0:
            while self.d.menu:
                menureturn = self.d.main_menu()
            if menureturn == 1:
                self.launch_game()
                self.d.menu = True
            if menureturn == 2:
                self.join_game()
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

    def join_game(self):
        self.launch_client()
        self.play_game()

    def launch_game(self):
        self.begin_game(create_earth())
        self.play_game()

    def pf(self,k,*args,**kwargs):
        T(self.d.win,str(k),0,0+self.toffset,200,200,200,center=False)# temporary, will be improved
        # with offsets described in self.toffset, and a nice buffer and background
        self.toffset = (self.toffset + 20) % 1000
        self.d.flip()

    def begin_game(self,w=earth,p=players,dut=default_unit_types):
        self.g = DGame(self.pf,w)
        self.setgdpipe() # now that the game is created
        self.g.set_p(p)
        # WILL BE CHANGED : YOU HAVE TO CHOOSE YOUR PLAYER
        self.player_otm = p[0]
        self.d.player_otm = self.player_otm
        # TODO
        self.g.dut = dut
        self.g.dstr = self.dstr
        self.g.begin()
        self.d.setmap(w.map)
        w.init_boxes()

    def join_game(self):
        w,p,dut = self.connect_to_game()
        self.g = DGame(self.pf,w)
        self.setgdpipe() # now that the game is created
        self.g.set_p(p)
        # WILL BE CHANGED : YOU HAVE TO CHOOSE YOUR PLAYER
        self.player_otm = p[1]# not the first
        self.d.player_otm = self.player_otm
        # TODO
        self.g.dut = dut
        self.g.dstr = self.dstr
        self.g.begin()
        self.d.setmap(w.map)
        w.init_boxes()

    def connect_to_game(self):
        self.net = NetworkClient(masterip)
        self.net.connect()

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
