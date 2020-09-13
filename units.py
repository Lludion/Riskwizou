## Units
from tools.printable import Printable
from random import randint

class Unit(Printable):

    def __init__(self, n, pm, d, c, z=None, own=None, bd=0, bo=0):
        self.name = n
        self.pm = pm #movement / point de mouvement
        self.d = d #dices / nombre de dés lancés
        self.c = c #cost / coût
        self.z = z #current zone / zone actuelle
        self.pmmax = pm
        self.boostd = bd
        self.boosto = bo
        self.owner = own
        self.id = randint(1, 99999999999999)

    def move(self, z):
        if self.pm > 0:
            if z.ntroops():
                pass
            else: #arriving on an empty territory
                z.owner = self.owner
                self.z.remove(self)
                self.z = z
                self.pm -= 1

    def attack(self):
        score = bo
        for _ in  range(self.d):
            score += randint(1,6)
        return score

    def defend(self):
        score = bd
        for _ in  range(self.d):
            score += randint(1,6)
        return score

    def __repr__(self):
        return self.__class__.__name__+"{"+self.name+"}\n"+str(self.d)+"D,"+str(self.pm)+"PM/"+str(self.pmmax)+"PMMAX[In "+str(self.z)+"]\n"

class Soldier(Unit):

    def __init__(self,z,own):
        super().__init__("soldier",1,1,1,z,own)

class Cavalry(Unit):

    def __init__(self,z,c):
        super().__init__("cavalry",2,1,2,z,c)

class Cannon(Unit):

    def __init__(self,z,c):
        super().__init__("cannon",1,2,2,z,c)

class Horde(Unit):

    def __init__(self,z,c):
        super().__init__("horde",3,1,2,z,c,1)

default_unit_types = (Soldier,Cavalry,Cannon)

