import socket
from _thread import *
import time
import FindMyIP as ip

class Server:
    def __init__(self):
        server = ip.internal()
        print("Hosting at "+str(ip.internal()+"."))
        port = 12348

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.s.bind((server, port))
        except socket.error as e:
            str(e)

        self.s.listen(2)
        print("Waiting for a connection, Server Started")


    def threaded_client(self, player):
        self.conn.send("Connected".encode("utf-8"))
        reply = "this is my message! "
        while True:
            try:
                data = self.conn.recv(2048).decode("utf-8")
                if not data:
                    print("Disconnected")
                    break
                else:
                    print("Received: ", data)
                    self.conn.sendall(str(player.getPos()).encode("utf-8"))
                    time.sleep(0.1)



            except:
                break

        print("Lost connection")
        self.conn.close()

  

    def startServer(self,player):


        while True:
            self.conn, addr = self.s.accept()
            print("hi")
            print("Connected to:", addr)

            self.threaded_client(player)


