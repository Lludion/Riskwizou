from networking import NetworkServer,masterip
from time import sleep

z = NetworkServer("")
print("CREATED")
z.launch()
while 1:
    z.accept()
    print("loop")
print("ENDED")
sleep(5)

sleep(2)
