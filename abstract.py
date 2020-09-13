import json

class Game:
    def __init__(self,w=None):
        """ Initialization """
        self.language = "french"
        self.w = w # world
        self.p = [] # players
        self.graphical = False
        with open("data/lang/"+self.language+".json", "r", encoding="utf-8-sig") as read_file:
            self.dict_str = json.load(read_file)

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
        for p in self.p:
            p.turn()