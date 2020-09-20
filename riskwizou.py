from random import randint,choice
from tools.printable import Printable
from tools.list import purify,forall
from tools.defeat import defeat
from tools.selection import szone
from tools.misc import atkwin

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
        self.claimed = None # no one claimed it yet
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
    
    def claim_prize(self,c,dut):
        """ allows a country to claim the prize for conquering this continent """
        if self.claimed is False:
            if forall(lambda x:x.owner == c,self.zones):
                self.claimed = c # the country c claimed it successfully
                pow = self.power
                while pow > 0:
                    if pow > 1:
                        c.capital.add_troop([dut[2]],c)
                        pow -= 2
                    else:
                        c.capital.add_troop([dut[0]],c)
                        pow -= 1
        
class World(Printable):
    
    def __init__(self, c, name =''):
        self.name = name
        for x in c:
            x.w = self
        self.continents = c
        self.map = ""
        self.natk = 3 
        self.ndef = 2
    
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
        self.terscore = 0
        self.uscore = 0
        self.combatscore = 0
    
    def score(self):
        return self.terscore + self.uscore + self.combatscore
    
    def new_capital(self):
        if self.capital is None:
            if self.units:
                self.capital = choice(self.units).z
            #else, self has lost.
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
    
    def units_arrival(self,chosen,dest,d=None):
        if dest.nforeign(self):
            # diplomacy will be implemented later, nwo we always attack
            if len(chosen) >= 3:
                print("Cannot attack with so many troops at once !")
                return
            print("Attackers :")
            atkscore = 0
            for u in chosen:
                atk,_ = u.attack()
                atkscore += atk
            print("Total : ",atkscore)
            
            print("Defenders :") # the defender should now select its two troops
            defscore = 0
            for u in dest.troops: # all foreign units are attacked
                atk,_ = u.defend()
                defscore += atk
            print("Total : ",defscore)
            
            if atkscore <= defscore:
                print("defenders win !")
                defeat(chosen)
            else:
                print("attackers win !")
                defeat(dest.troops,"no") # all troops are killed
                atkwin(dest,chosen)

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
    
    def owned(self):
        ownz = []
        for c in self.w.continents:
            for z in c.zones:
                if z.owner == self:
                    ownz.append(z)
        return ownz

class Country(ConsoleCountry):
    
    def __init__(self,n,c=(0,0,0)):
        super().__init__(n,c)
        self.graphical = True #is a Graphical Country
        self.cu_step = 0
        self.cu_zone = None
        self.action = ''
    
    def begin_turn(self,d):
        self.terscore = 0
        for z in self.owned():
            self.terscore += 10
            if z.cont.claimed == self:
                self.terscore += 10
            if forall(lambda x: x.owner == self,z.cont.zones):
                self.terscore += 10
        self.uscore = sum([u.d for u in self.units])
        if self.g.turn_num > 0:
            if d.key_s():
                uc = 0
            elif d.key_d():
                uc = 1
            elif d.key_f():
                uc = 2
            else:
                uc = randint(0,2)
            if uc == 0:
                self.capital.add_troop([self.g.dut[0],self.g.dut[0]],self)
                d.announce("gsoldier")
            else:
                self.capital.add_troop([self.g.dut[uc]],self)
                if uc == 1:
                    d.announce("gcavalier")
                elif uc == 2:
                    d.announce("gcannon")

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
            #print("cu1")
            d.zonebox(self.cu_zone)
            self.cu_step = d.clicked_on_unit(self.cu_zone)
        elif self.cu_step == 2:#one-frame-temporary stuff
            #print("cu2")
            assert d.selectedunits[0].z == self.cu_zone
            self.selecta = d.selectedunits
            d.selectedunits = []
            d.printedunits = []
            self.cu_step = 3
        elif self.cu_step == 3:#choosing the zone where you want to move
            #print("cu3")
            d.zonebox(self.cu_zone,["moving"])
            self.cu_step = self.move_units(self.selecta,self.cu_zone,mp,d)
        elif self.cu_step == 4:#choosing the defender's units
            self.cu_step = self.units_arrival(self.selecta,self.dest,d)
        else:
            print("omegapharma",self.cu_step)
            d.selectedunits = []
            d.printedunits = []
            self.action = ""
            self.cu_step = 0
    
    def move_units(self,chosen,gofrom,mp,d):
        if d.flclic():
            self.dest = szone(mp,self.w)
            if self.dest in self.cu_zone.adj:
                return self.units_arrival(chosen,self.dest,d)
            else:
                return 3
        return 3
        
    def units_arrival(self,chosen,dest,d):
        if dest is None:
            return 3 # redo the choice of the destination
        if dest.nforeign(self):
            # diplomacy will be implemented later, nwo we always attack

            if len(chosen) > self.w.natk:
                self.g.s("Cannot attack with so many troops at once !")
                return -1
            # the defender should now select its two troops
            if dest.ntroops() > self.w.ndef:
                if len(d.selectedunits) < self.w.ndef:
                    # if a choice is possible and not everyone has been chosen:
                    d.zonebox(dest,["defenderchoice"])
                    arrivstep = d.select_units(dest)
                    if arrivstep == 2:
                        dtroops = d.selectedunits
                        d.selectedunits = []
                    else:#keep choosin'
                        return 4
                else:
                    dtroops = d.selectedunits
                    d.selectedunits = []
                    
            else:
                dtroops = dest.troops
            d.display_fight()
            print("Defenders :") 
            defscore = 0
            j = 0
            for u in dtroops: # the selected foreign units are attacked
                atk,j = u.defend(d,j)
                defscore += atk
            print("Total : ",defscore)
            
            d.display_fight(None)
            print("Attackers :")
            atkscore = 0
            j = 0
            for u in chosen:
                atk,j = u.attack(d,j,None)
                atkscore += atk
            print("Total : ",atkscore)
        
            if atkscore <= defscore:
                print("defenders win !")
                dtroops[0].owner.combatscore += sum([u.d for u in chosen])
                defeat(chosen)
                if d.player_otm == self.p:
                    d.announce("gdefeat")
                else:
                    d.announce("gvictory")
            else:
                print("attackers win !")
                self.combatscore += sum([u.d for u in chosen])
                defeat(dtroops,"no") # all troops are killed
                #if dest.troops == []: # invasion
                #    self.combatscore += 1 # currently removed for balance reasons
                atkwin(dest,chosen)
                if d.player_otm == self.p:
                    d.announce("gvictory")
                else:
                    d.announce("gdefeat")
            return -1

        else:
            for u in chosen:
                u.move(dest)
            return -1
    
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
    
    def end_turn(self,d=None):
        for c in self.w.continents:
            if forall(lambda x: x.owner is self, c.zones):
                c.claim_prize(self,self.g.dut)

class Player(Printable):
    
    def __init__(self, n, c):
        self.name = n
        self.countries = c #One player may control several countries
        self.g = None
    
    def get_countries(self,new):
        self.countries += new
        for c in self.countries:
            c.p = self

