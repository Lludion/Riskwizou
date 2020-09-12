from  random import randint

class Zone :

    def __init__(self, n, a, c):
        self.name=n
        self.adj=a
        self.cont=c
        self.troops=[]
        self.owner=None
        
    def ntroops(self):
        return len(self.troops)
        
    def remove(self, unit):
        self.troops= [x for x  in self.troops if  x.id  !=  unit.id]
        
class Cont:
    
    def __init__(self, n, p, z):
        self.name=n
        self.power=p
        self.zones=z
        
class World:
    
    def __init__(self, c):
        self.continents=c
        
class Unit:
    
    def __init__(self, n, pm, d, z, own, bd=0, bo=0):
        self.name=n
        self.pm=pm#point de mouvement
        self.d=d#nombre de dés lancés
        self.z=z#zone actuelle
        self.pmmax=pm
        self.boostd=bd
        self.boosto=bo
        self.owner=own
        self.id=randint(1, 99999999999999)
        
    def move(self, z):
        if self.pm>0:
            if z.ntroops():
                pass
            else:
                z.owner=self.owner
                self.z.remove(self)
                self.z=z
                self.pm-=1
            
    def attack(self):
        score=bo
        for _ in  range(self.d):
            score+=randint(1,6)
        return score 
         
    def defend(self):
        score=bd
        for _ in  range(self.d):
            score+=randint(1,6)
        return score
        
class Player:
    
    def __init__(self, c, n):
        self.color=c
        self.units=[]
        self.name=n
    
    def turn(self):
        pass
    
    def attack(self, units, enemy):
        if units!=[]:
            uzone=units[0]
            #foralltheKaK
            if len(enemy)>self.w.ndef:
                print("nombre maximal de défenseur dépassé!")
            else:
                atkscore=sum