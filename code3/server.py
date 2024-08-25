import socket
from _thread import *
import FindMyIP as ip

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


def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = "this is a message! "
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")
            
            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()

def startServer():
    while True:
        conn, addr = s.accept()
        print("hi")
        print("Connected to:", addr)

        threaded_client, (conn,)
