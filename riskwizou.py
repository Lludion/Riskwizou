from random import randint

class Zone :

    def __init__(self, n, c, a=[]):
        self.name = n
        self.adj = a
        self.activeadj = [True for s in self.adj]
        self.cont = c
        self.troops = []
        self.owner = None #Country
        
    def ntroops(self):
        return len(self.troops)
        
    def remove(self, unit):
        self.troops = [x for x  in self.troops if  x.id  !=  unit.id]
        
class Cont:
    
    def __init__(self, n, p, z=[]):
        self.name = n
        self.power = p
        self.zones = z
    
    def add(self,z):
        """ adding a zone to the continent"""
        if type(z) == type(""):
            newzone = Zone(z,self)
        else:
            newzone = z
        
        newzone.cont = self
        self.zones.append(newzone)
    
    def adds(self,list):
        """ adding several zones """
        for z in list:
            self.add(z)
            
    def __getitem__(self, item):
        if type(item) == type(""):
            for z in self.zones:
                if z.name == item:
                    return z
        else:
            for z in self.zones:
                if z.name == item.name:
                    return z

class World:
    
    def __init__(self, c=[]):
        self.continents=c

    def __getitem__(self, item):
        for z in self.continents:
            if z[item] is not None:
                return z[item]
        
class Unit:
    
    def __init__(self, n, pm, d, z, own, bd=0, bo=0):
        self.name = n
        self.pm = pm #point de mouvement
        self.d = d #nombre de dés lancés
        self.z = z #zone actuelle
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

class Country:
    def __init__(self, n, c=(0,0,0)):
        self.units = []
        self.name = n
        self.color = c

class Player:
    
    def __init__(self, n, c):
        self.name = n
        self.countries = c #One player may control several countries
    
    def turn(self):
        pass
    
    def attack(self, units, enemy):
        if units != []:
            uzone = units[0]
            #foralltheKaK
            if len(enemy) > self.w.ndef:
                print("nombre maximal de défenseurs dépassé!")
            else:
                atkscore = sum([unit.attack() for unit in units])
                defscore = sum([unit.defend() for unit in enemy])
