from random import randint,choice
from tools.printable import Printable
from tools.list import purify
from tools.defeat import defeat
from tools.selection import szone

class Zone(Printable) :

    def __init__(self, n, c):
        self.name = n
        self.adj = []
        self.activate()
        self.cont = c
        self.troops = []
        self.owner = None #Country
        self.boxes = []
    
    def ab(self,xm,xM,ym,yM):
        """add box"""
        self.boxes.append((xm,xM,ym,yM))
    
    def center(self):
        """ returns a tuple of pixels in the size of the real map (usually 4000x2640)"""
        if self.boxes:
            return (self.boxes[0][0]+self.boxes[0][1])//2,(self.boxes[0][2]+self.boxes[0][3])//2
        else:
            return 0,0
        
    def ntroops(self):
        return len(self.troops)
    
    def add_troop(self,type,c):
        if isinstance(type,list):
            for u in type:
                un = u(self,c) # creating a unit
                self.troops.append(un)
                c.units.append(un)
        else:
            un = type(self,c)
            self.troops.append(un)
            c.units.append(un)

    def remove(self, unit):
        self.troops = [x for x in self.troops if  x.id  !=  unit.id]
    
    def nforeign(self,c):
        """ number of foreigners in self, wrt the country c """
        return len([u for u in self.troops if u.owner != c])
        
    def add_conn(self,z):
        """ adds a connection to the zone z 
        and a connection to self in z"""
        self.adj.append(z)
        z.adj.append(self)
    
    def add_conns(self,*L):
        """ adds connections to the zones in L"""
        for z in L:
            if type(z) == type(""):
                self.add_conn(self.cont.w[z])
            else:
                self.add_conn(z)
    
    def print_conns(self):
        print(self.name + "-> " + str(self.adj))
    
    def activate(self):
        self.activeadj = [True for s in self.adj]
        
        
class Cont(Printable):
    
    def __init__(self, n, p):
        self.name = n
        self.power = p
        self.zones = []
        self.w = None # world
    
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
                try:
                    if z.name == item.name:
                        return z
                except AttributeError:
                    return None
    
    def print_conns(self):
        for z in self.zones:
            z.print_conns()
        
class World(Printable):
    
    def __init__(self, c, name =''):
        self.name = name
        for x in c:
            x.w = self
        self.continents = c
        self.map = ""
    
    def init_boxes(self):
        szone((-1,-1),self) # initializing the boxes
    
    def setmap(self,map):
        self.map = map

    def __getitem__(self, item):
        for z in self.continents:
            if z[item] is not None:
                return z[item]
    
    def purify_transitions(self):
        for c in self.continents:
            for z in c.zones:
                z.adj = purify(z.adj)
    
    def activate_transitions(self):
        for c in self.continents:
            for z in c.zones:
                z.activate()

class ConsoleCountry(Printable):
    def __init__(self, n, c=(0,0,0)):
        self.units = []
        self.name = n # all countries must have a different name
        self.color = c
        self.p = None # player
        self.g = None # game
        self.w = None # world
        self.graphical = False #is a Console Country
        self.capital = None
    
    def new_capital(self):
        if self.capital is None:
            self.capital = choice(self.units).z
        elif self.capital.owner != self:
            self.capital.owner = self
        else:
            raise FutureWarning("Called new_capital without any reason, the capital is already : " + str(self.capital) + ", owned by " + str(self))
    
    def choose_units(self):
        
        ch = []
        z = self.w.continents[0].zones[0]
        if self.graphical:
            print("~~GRAPHICAL~~")
            print("YOU SHOULDN'T USE THIS CLASS IN GRAPHICAL MODE'")
        else:
            z = None # zone
            for u in self.units:
                u.info()
                if (z is None or z == u.z) and u.pm >= 1:
                    if input("Do you select this unit?"):
                        z = u.z
                        ch.append(u)
                else:
                    print("(Unité non sélectionable)")
        print("sélectionné: "+str(ch))
        return ch, z
        
    def turn(self):
        if not self.units: # no units
            return
        elif not [x for x in self.g.c if x != self and x.units]:
            #no one else has units
            print(self.name, "won !")
            self.g.ended = True
            return
        #not graphical
        print("Turn of "+self.name)
        turn = True
        for u in self.units:
            u.pm = u.pmmax # restoring pm
        while turn:
            print("What do you want to do?")
            ch = input("m for move, e for end the turn, q for quit ")
            if "q" in ch or "Q" in ch:
                turn = False
                self.g.ended = True
            elif "e" in ch or "E" in ch:
                turn = False
            else:
                chosen,gofrom = self.choose_units()
                self.move_units(chosen,gofrom)
        
    def move_units(self,chosen,gofrom):
        if chosen:
            print("Where do you want to go?")
            for i in range(len(gofrom.adj)):
                print(str(i)+" : "+str(gofrom.adj[i]),"(",gofrom.adj[i].nforeign(self),"foreigners)")
            try:
                i = int(input("Entrer le numero de la destination:"))
            except ValueError:
                i = -1 # to always enter the loop
            finally:
                while i != i % len(gofrom.adj):
                    try:
                        i = int(input("Entrer le numero de la destination (<"+str(len(gofrom.adj))+"):"))
                    except ValueError:
                        i = -1 # to always re-enter the loop
                dest = gofrom.adj[i]
                self.units_arrival(chosen,dest)
        else:
            print("No Units selected.")
    
    def units_arrival(self,chosen,dest):
        if dest.nforeign(self):
            # diplomacy will be implemented later
            print("Attackers :")
            atkscore = 0
            for u in chosen:
                atk = u.attack()
                atkscore += atk
            print("Total : ",atkscore)
            
            print("Defenders :")
            defscore = 0
            for u in dest.troops: # all foreign units are attacked
                atk = u.attack()
                defscore += atk
            print("Total : ",defscore)
            
            if atkscore <= defscore:
                print("defenders win !")
                defeat(chosen)
            else:
                print("attackers win !")
                defeat(dest.troops,"no") # all troops are killed
                for u in chosen:
                    u.move(dest)

        else:
            for u in chosen:
                u.move(dest)
    
    def attack(self, units, enemy):
        if units != []:
            uzone = units[0]
            #foralltheKaK
            if len(enemy) > self.w.ndef:
                print("nombre maximal de défenseurs dépassé!")
            else:
                atkscore = sum([unit.attack() for unit in units])
                defscore = sum([unit.defend() for unit in enemy])

    def remove(self, unit):
        self.units = [x for x in self.units if  x.id  !=  unit.id]


class Country(ConsoleCountry):
    
    def __init__(self,n,c=(0,0,0)):
        super().__init__(n,c)
        self.graphical = True #is a Graphical Country
        self.cu_step = 0
        self.cu_zone = None
        self.action = ''

    def choose_units(self,mp,d):
        """ This function is used when m is being pressed. 
        It manages the several steps of unit selection.
        1) zone selection
        2) unit selection within the zone """
        if self.cu_step == 0:#choosing a zone
            if d.flclic():
                z = szone(mp,self.w)
                if z is not None:
                    print("z",z)
                    self.cu_step = 1
                    self.cu_zone = z
                else:
                    self.cu_zone = None
        elif self.cu_step == 1:#choosing the units
            print("1")
            d.zonebox(self.cu_zone)
            self.cu_step = d.clicked_on_unit(self.cu_zone)
        elif self.cu_step == 2:#choosing the zone where you want to move
            print("2")
            assert d.selectedunits[0].z == self.cu_zone
            self.move_units(d.selectedunits,self.cu_zone,mp,d)
        else:
            print("omegapharma",self.cu_step)
            d.selectedunits = []
            d.printedunits = []
            self.action = ""
            self.cu_step = 0
    
    def move_units(self,chosen,gofrom,mp,d):
        if d.flclic():
            self.units_arrival(chosen,szone(mp,self.w))
            self.cu_step = -1
    
    def turn(self,d):
        """
        d is the displayer that will be used
        """
        self.g.s("Turn of "+self.name)
        turn = True
        for u in self.units:
            u.pm = u.pmmax # restoring pm
        while turn:
            mp = d.game()
            if self.action == "choose_units":
                self.choose_units(mp,d)
            else:
                d.zonebox(self.cu_zone)
                for event in d.pygame.event.get():
                    if event.type == d.pygame.KEYDOWN:
                        if event.key == d.pygame.K_ESCAPE:
                            turn = False
                            self.g.ended = True
                        if event.key == d.pygame.K_e:
                            turn = False                            
                        if event.key == d.pygame.K_c:
                            self.action = "choose_units"
                    if event.type == d.pygame.MOUSEBUTTONDOWN:
                        self.cu_zone = szone(mp,self.w)

class Player(Printable):
    
    def __init__(self, n, c):
        self.name = n
        self.countries = c #One player may control several countries
        self.g = None
    
    def get_countries(self,new):
        self.countries += new
        for c in self.countries:
            c.p = self

