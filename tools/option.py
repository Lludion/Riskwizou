
class Option:

    def __init__(self,arg):
        self.cx = False # center x
        self.cy = False # center y
        self.announce = False # announce (only one at a time)
        self.x = 0
        self.y = 0
        if "x" == arg[0]:
            self.cx = True
            arg = arg[1:]
        if "y" == arg[0]:
            self.cy = True
            arg = arg[1:]
        if "a" == arg[0]:
            self.announce = True
            arg = arg[1:]
        a = ""
        b = ""
        adb = False
        for x in arg:
            if x == ",":
                adb = True
            elif adb:
                b += x
            else:
                a += x
        try:
            self.x = int(a)
        except:
            pass
        try:
            self.y = int(b)
        except:
            pass
        print("xy",self.x,self.y)
