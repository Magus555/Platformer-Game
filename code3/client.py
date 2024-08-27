import socket
import threading
import time


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.0.0.29"
        self.port = 12348
        self.addr = (self.server, self.port)


    def connect(self,player):
        self.client.connect(self.addr)
        while True:
            try:
                data = self.client.recv(2048).decode("utf-8")
                if not data:
                    break
                print(data)
                self.client.sendall(str(player.getPos()).encode("utf-8"))
            except socket.error as e:
                print(e)
                break
        
        print("Lost connection")
        self.client.close()

    def send(self, data):
        try:
            self.client.sendall(str(data).encode("utf-8"))
        except socket.error as e:
            print(e)
            return


