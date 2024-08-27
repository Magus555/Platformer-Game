import socket
from _thread import *
import time
import FindMyIP as ip

class Server:
    def __init__(self):
        server = ip.internal()
        print("Hosting at "+str(ip.internal()+"."))
        self.port = 12348

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)

        try:
            self.sock.bind((server, self.port))
        except socket.error as e:
            str(e)

        print("Waiting for a connection, Server Started")

        self.playerPos = 0
        self.lastPlayerPos = 0


    def threaded_client(self, player, otherPlayer):
        reply = "this is my message! "
        while True:
            try:
                data,address = self.sock.recvfrom(2048)
                print(data)
                break
            except:
                time.sleep(5)
                pass


        while True:
            try:
                try:
                    data = self.sock.recv(2048)
                except:
                    data = ""

                if not data:
                    pass
                else:
                    data=data.decode('utf-8')
                    print("Received: ", data)
                    if(len(data.split('('))>1):
                        x=data.split('(')[1].split(',')[0]
                        y=data.split(')')[0].split(',')[1]
                        otherPlayer.setPos(x,y)

                self.playerPos = player.getPos()
                if(self.playerPos!=self.lastPlayerPos):
                    print("triggered")
                    self.lastPlayerPos=self.playerPos
                    self.sock.sendto(str(self.playerPos).encode("utf-8"), address)
                    time.sleep(0.01)

                        





            except:
                break

        print("Lost connection")
        self.sock.close()

  

    def startServer(self,player,otherPlayer):


        while True:


            self.threaded_client(player,otherPlayer)


