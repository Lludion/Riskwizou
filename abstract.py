from random import choice
from net.networking import NetworkServer, NetworkClient

class Game:
    def __init__(self,w=None):
        """ Initialization """
        self.w = w # world
        self.p = [] # players
        self.c = [] # countries
        self.dut = (None,None,None) # default unit types
        self.graphical = False
        self.ended = False
        self.s = print # show function is print by default

    def set_p(self,players):
        """ given a set of players, sets self.p and self.c (players and countries) """
        self.p = []
        self.c = []
        for p in players:
            self.p.append(p)
            p.g = self
            for c in p.countries:
                self.c.append(c)
                c.g = self
                c.p = p
                c.w = self.w

    def begin(self):
        self.s(self.c)
        self.__set_startzones()

    def __randomzone(self):
        # return choice(choice(self.w.continents).zones)
        return choice((self.w.continents[5]).zones)

    def __set_startzones(self):
        szs = [] # startzones
        for c in self.c:
            startzone = self.__randomzone()
            self.s(startzone)
            safe = 150
            while (startzone in szs) and safe: # may fail for huge number of players
                startzone = self.__randomzone()
                safe -= 1
            if not safe:
                self.s("ERROR : TOO MANY PLAYERS ! The map is full !")
                self.s("Suppressing country "+str(c))
                del c
            else:
                szs.append(startzone)
                for i in (0,1,2):
                    startzone.add_troop(self.dut[i],c)

    def turn(self):
        for c in self.c:
            c.turn()
            if self.ended:
                return

class DGame(Game):

    def __init__(self,pf,w=None):
        super().__init__(w=w)
        self.s = pf # print function

    def turn(self):
        """ the c must be Countries and not ConsoleCountries """
        for c in self.c:
            c.turn(self.d)
            if self.ended:
                return

class Networker:

    def __init__(self,host="127.0.0.1"):
        self.srv = NetworkServer(host)
        self.cli = NetworkClient(host)

