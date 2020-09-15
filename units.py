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
        self.has_attacked = False
        self.id = randint(1, 99999999999999)

    def beginturn(self):
        if self.z.owner is None: # useful for abandoning province while having friendly armies present
            self.z.owner = self.owner
        self.has_attacked = False

    def move(self, z):
        if self.pm > 0:
            print("Troops number in",z,z.ntroops())
            if z.nforeign(self.owner):
                # This is not the place where to check this, as we attack
                # in large numbers !
                raise FutureWarning("A check for foreigners in Unit.move saw an unexpected result.")
            else: #arriving on an empty territory
                self.z.remove(self)
                self.z = z
                self.pm -= 1
                print(z,z.owner)
                z.owner = self.owner
                z.troops.append(self)
                print(z,z.owner)

    def attack(self):
        self.has_attacked = True
        scores = []
        txt = str(self) + " did "
        for i in  range(self.d):
            if i:
                txt += "+ "
            scores.append(randint(1,6))
            txt += str(scores[-1]) + " "
        if  self.boosto:
            txt += "+ 1 (boost) "
        if len(scores) >= 2:
            txt += "(=" + str(sum(scores) +  self.boosto) + ") "
        txt += "!"
        print(txt)
        return sum(scores) +  self.boosto

    def defend(self):
        scores = []
        txt = str(self) + " did "
        for i in  range(self.d):
            if i:
                txt += "+ "
            scores.append(randint(1,6))
            txt += str(scores[-1]) + " "
        if  self.boostd:
            txt += "+ 1 (boost)"
        if len(scores) >= 2:
            txt += "(=" + str(sum(scores) +  self.boosto) + ") "
        txt += "!"
        print(txt)
        return sum(scores) + self.boostd

    def info(self):
        print( self.__class__.__name__+"{"+self.name+"}\n"+str(self.d)+"D,"+str(self.pm)+"PM/"+str(self.pmmax)+"PMMAX[In "+str(self.z)+"]\n" )

    def dies(self):
        self.z.remove(self)
        self.z = None
        self.owner.remove(self)
        self.owner = None
        del self

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

