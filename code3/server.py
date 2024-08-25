import socket
from _thread import *
import time
import FindMyIP as ip
import pygame



def threaded_client(conn, q):
    clock = pygame.time.Clock()
    clock.tick(60)
    conn.send("Connected".encode("utf-8"))
    reply = "this is my message! "
    while True:
        try:
            data = conn.recv(2048).decode("utf-8")
            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", data)
                if(q.empty()==False):
                    reply = q.get()
                    print("Sending : ", reply)
                    conn.sendall(str(reply).encode("utf-8"))
                    
                else:
                    pass
               

        except:
            break

    print("Lost connection")
    conn.close()


def startServer(q):

    server = ip.internal()
    print("Hosting at "+str(ip.internal()+"."))
    port = 12348

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)

    s.listen(2)
    print("Waiting for a connection, Server Started")
    while True:
        conn, addr = s.accept()
        print("hi")
        print("Connected to:", addr)

        threaded_client(conn,q)
