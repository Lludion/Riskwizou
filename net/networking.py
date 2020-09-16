import socket

class NetInterface:

    def __init__(self,host='127.0.0.1',port=23074):
        self.host = host  # Default loopback interface address (localhost)
        self.port = port  # Port to listen on (unused according to wikipedia)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class NetworkServer(NetInterface):

    def __init__(self,host='127.0.0.1',port=23074):

        super().__init__(host,port)

    def launch(self):

        try:
            self.s.bind((self.host, self.port))
            print("BINDED")
            self.s.listen()
            print("LISTENED")
        except OSError as e:
            print("OSError: ",e)
            print("No bind created, no server launched.")

    def accept(self):
        conn, addr = self.s.accept()
        print("ACCEPTED")
        with conn:
            print('Connected by', addr)
            new = conn.recv(1024)
            data = "" + new
            while new:
                print("DATA:",data)
                conn.sendall(data)
                new = conn.recv(1024)
                data += new
        return data

    def close_socket(self):
        self.s.close()

class NetworkClient(NetInterface):

    def __init__(self,host='127.0.0.1',port=23074):

        super().__init__(host,port)

    def connect():
        self.s.connect((self.host, self.port))

    def send(self,msg=None):
        if msg is None:
            msg = b'The invasion was a surprise attack, described by Allied forces as rapid and conducted with ease. Prior to the invasion, two diplomatic notes were delivered to the Iranian government on 19 July and 17 August, requiring the Iranian government to expel German nationals. The second of the notes was recognised by the prime minister Ali Mansur as a disguised ultimatum. General Archibald Wavell later wrote in his despatch, "it was apparent that the Iranian Government fully expected an early British advance into Khuzistan and that reinforcements, including light and medium tanks, were being sent to Ahvaz".Soviet and Indian soldiers meet in late August.Following the invasion, Sir Reader Bullard and Andrey Andreyevich Smirnov, the British and Soviet ambassadors to Iran, were summoned. The Shah demanded to know why they were invading his country and why they had not declared war. Both answered that it was because of "German residents" in Iran. When the Shah asked if the Allies would stop their attack if he expelled the Germans, the ambassadors did not answer. The Shah sent a telegram to the US President Franklin D. Roosevelt, pleading with him to stop the invasion. As the neutral United States had nothing to do with the attack, Roosevelt was not able to grant the Shah s plea but stated that he believed that the territorial integrity of Iran should be respected.The Royal Navy and Royal Australian Navy attacked from the Persian Gulf while other British Commonwealth forces came by land and air from Iraq. The Soviet Union invaded from the north, mostly from Transcaucasia, with the 44th, 47th armies of the Transcaucasian Front (General Dmitry Timofeyevich Kozlov), and 53rd army of the Central Asian Military District, occupying Irans northern provinces. Air force and naval units also participated in the battle. The Soviets used about 1,000 T-26 tanks for their combat operations.Six days after the invasion and the ensuing Allied occupation of southern Iran, the British divisions previously known as "Iraq Command" (also known as Iraqforce) were renamed "Persia and Iraq Force" (Paiforce), under the command of Lieutenant-General Edward Quinan. Paiforce was made up of the 8th and 10th Indian Infantry divisions, the 2nd Indian Armoured Brigade, 4th British Cavalry Brigade (later renamed 9th Armoured Brigade) and the 21st Indian Infantry Brigade. The invading Allies had 200,000 troops and modern aircraft, tanks, and artillery.'

        self.s.sendall(msg)
        data = self.s.recv(1024)

        print('Received', repr(data))

    def close_socket(self):
        self.s.close()
