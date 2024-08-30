import socket
import threading
import time


class Network:
    def __init__(self,connected):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.setblocking(False)
        self.server = "10.0.0.29"
        self.port = 12348
        self.addr = (self.server, self.port)
        self.playerPos=0
        self.lastPlayerPos=0
        self.connected = connected

    def connect(self,player,otherPlayer):
        self.client.sendto("Connected".encode('utf-8'), self.addr)
        while True:
            try:
                try:
                    data = self.client.recv(2048).decode("utf-8")
                except:
                    data = ""

                if not data:
                    pass
                else:

                    print("Received: ", data)
                    if(len(data.split('('))>1):
                        x=data.split('(')[1].split(',')[0]
                        y=data.split(')')[0].split(',')[1]
                        otherPlayer.setPos(x,y)
                        self.connected.put(True)

                self.playerPos = player.getPos()
                if(self.playerPos!=self.lastPlayerPos):
                    self.lastPlayerPos=self.playerPos
                    self.client.sendto(str(self.playerPos).encode("utf-8"), self.addr)
                    time.sleep(0.01)

            except socket.error as e:
                print(e)
                break
        
        print("Lost connection")
        self.client.close()

    def send(self, data):
        try:
            self.client.sendto(str(data).encode("utf-8"),self.addr)
        except socket.error as e:
            print(e)
            return


