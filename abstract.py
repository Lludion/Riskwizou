

class Game:
    def __init__(self):
        """ Initialization """

        with open("data/lang/french.json", "r", encoding="utf-8-sig") as read_file:
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