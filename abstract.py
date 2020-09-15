import json
from random import choice

class Game:
    def __init__(self,w=None):
        """ Initialization """
        self.language = "french"
        self.w = w # world
        self.p = [] # players
        self.c = [] # countries
        self.dut = (None,None,None) # default unit types
        self.graphical = False
        self.ended = False
        with open("data/lang/"+self.language+".json", "r", encoding="utf-8-sig") as read_file:
            self.dict_str = json.load(read_file)

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
        print(self.c)
        self.__set_startzones()

    def __randomzone(self):
        # return choice(choice(self.w.continents).zones)
        return choice((self.w.continents[5]).zones)

    def __set_startzones(self):
        szs = [] # startzones
        for c in self.c:
            startzone = self.__randomzone()
            print(startzone)
            safe = 150
            while (startzone in szs) and safe: # may fail for huge number of players
                startzone = self.__randomzone()
                safe -= 1
            if not safe:
                print("ERROR : TOO MANY PLAYERS ! The map is full !")
                print("Suppressing country "+str(c))
                del c
            else:
                szs.append(startzone)
                for i in (0,1,2):
                    startzone.add_troop(self.dut[i],c)

    def dstr(self,char):
        """ Try to find if dict_str contains a value for the key 'char'.
        If not, it  returns the char value itself.
        This function is to be used with numbers, and strings when we do not
        know at compile time whether they will be in dict_str or not."""
        try:
            return self.dict_str[char]
        except KeyError:
            return char

    def turn(self):
        for c in self.c:
            c.turn()
            if self.ended:
                return