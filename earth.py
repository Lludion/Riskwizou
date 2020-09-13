from riskwizou import *
from abstract import *

game = Game()

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
europe.adds(["iceland",'greatbritain',"scandinavie","ukraine","north","south","west"])

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


