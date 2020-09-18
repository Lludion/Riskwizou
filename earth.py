from riskwizou import World,Zone,Cont,Country,Player

def create_earth():
    ## Continents

    na = Cont("northamerica",5)
    sa = Cont("sourthamerica",2)
    asia = Cont("asia",7)
    europe = Cont("europe",5)
    africa = Cont("africa",3)
    oceania = Cont("oceania",2)

    ##Zones

    #North america
    alaska = Zone("alaska",na)
    nunavut = Zone("nunavut",na)
    alberta = Zone("alberta",na)
    ontario = Zone("ontario",na)
    quebec = Zone("quebec",na)
    westernstates = Zone("westernstates",na)
    easternstates = Zone("easternstates",na)
    centralamerica = Zone("centralamerica",na)
    groenland = Zone("groenland",na)
    na.adds([alaska,nunavut,alberta,ontario,quebec,westernstates,easternstates,centralamerica,groenland])

    #Europe
    europe.adds(["iceland",'greatbritain',"scandinavia","ukraine","north","south","west"])

    #Asia
    asia.adds(["afghanistan","ural","siberia","tchita","mongolia","yakutia","china","japan","kamschatka","middleeastern","india","siam"])

    #Oceania
    oceania.adds(["indonesia","newguinea","eastaustralia","westaustralia"])

    #Africa
    africa.adds(["congo","madagascar","egypt","northafrica","eastafrica","southafrica"])

    #South America
    sa.adds(["brasil","peru","venezuela","argentina"])

    #earth
    earth = World([na,sa,asia,europe,africa,oceania])

    ## Connections

    #North America

    earth["alaska"].add_conns(earth["kamschatka"],earth["nunavut"],earth["alberta"])
    earth["alberta"].add_conns(earth["nunavut"],earth["ontario"],earth["westernstates"])
    earth["ontario"].add_conns(earth["nunavut"],earth["groenland"],earth["quebec"],earth["easternstates"],earth["westernstates"])
    earth["groenland"].add_conns(earth["nunavut"],earth["quebec"],earth["iceland"])
    earth["easternstates"].add_conns(earth["quebec"],earth["westernstates"],earth["centralamerica"])
    earth["centralamerica"].add_conns(earth["easternstates"],earth["westernstates"],earth["venezuela"])

    #Europe

    earth["iceland"].add_conns(earth["scandinavia"],earth["greatbritain"])
    earth["greatbritain"].add_conns(earth["scandinavia"],earth["west"],earth["north"])
    earth["scandinavia"].add_conns(earth["north"],earth["ukraine"])
    earth["north"].add_conns(earth["south"],earth["west"],earth["ukraine"])
    earth["south"].add_conns(earth["west"],earth["ukraine"])

    #Asia

    earth["ural"].add_conns(earth["ukraine"],earth["afghanistan"],"china","siberia")
    earth["china"].add_conns("mongolia","afghanistan","siberia","india","siam")
    earth["tchita"].add_conns("mongolia","siberia","yakutia","kamschatka")
    earth["japan"].add_conns("mongolia","kamschatka")
    earth["middleeastern"].add_conns("ukraine","egypt","afghanistan","india","eastafrica")
    earth["siam"].add_conns("india","indonesia")

    #Oceania
    earth["westaustralia"].add_conns("newguinea","eastaustralia","madagascar","indonesia")
    earth["newguinea"].add_conns("indonesia","eastaustralia")

    #Africa
    earth["madagascar"].add_conns("southafrica","eastafrica")
    earth["congo"].add_conns("southafrica","eastafrica","northafrica")
    earth["egypt"].add_conns("eastafrica","northafrica","south")
    earth["northafrica"].add_conns("west","brasil","eastafrica")
    earth["southafrica"].add_conns("eastafrica")

    #South America
    earth["brasil"].add_conns("venezuela","argentina","peru")
    earth["peru"].add_conns("venezuela","argentina")

    #global
    earth.purify_transitions()
    earth.activate_transitions()
    earth.setmap("worldmap")
    return earth

## Players & Countries
earth = create_earth()
blue = Country("blue", (10,0,150))
red = Country("red", (150,10,0))
players = [Player("blue",[blue]), Player("red",[red])]

