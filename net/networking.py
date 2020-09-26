import socket
try:
    from tools import placeholder
except ModuleNotFoundError:
    class ____z:
        def __init__(s):
            s.bytes = b"placeholder"
    placeholder = ____z()
masterip = "2a01:cb10:8342:9b00:4984:ee5:75b8:8819"
#sometimes "2a01:cb10:8342:9b00:b574:b21f:fc2c:b948"
defaultport = 23074

class NetInterface:

    def __init__(self,host='localhost',port=defaultport):
        self.host = host  # Default loopback interface address (localhost)
        self.port = port  # Port to listen on (unused according to wikipedia)

        self.s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

class NetworkServer(NetInterface):

    def __init__(self,host='localhost',port=defaultport):

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
            data = b"" + new # bytes
            while new:
                print("DATA:",data)
                conn.sendall(data)
                new = conn.recv(1024)
                data += new
        return data

    def close_socket(self):
        self.s.close()

class NetworkClient(NetInterface):

    def __init__(self,host='localhost',port=defaultport):

        super().__init__(host,port)

    def connect(self):
        try:
            self.s.connect((self.host, self.port))
        except TimeoutError as e:
            print(TimeoutError.__name__,e)
            self.connect()

    def send(self,msg=None):
        if msg is None:
            msg = placeholder.bytes

        self.s.sendall(msg)

    def recv(self):
        data = self.s.recv(1024)
        print('Received', repr(data))

    def close_socket(self):
        self.s.close()
