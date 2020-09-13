from abstract import *
from earth import earth,players
from units import default_unit_types

# to test purity:
# print(earth.continents[0].zones[7].adj)

game = Game(earth)
game.set_p(players)
game.dut = default_unit_types

game.begin()
while not game.ended:
    game.turn()