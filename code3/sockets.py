import socket
import asyncio

async def hostServer():

    s = socket.socket()
    print("Socket successfully created")

    port = 12345

    s.bind(('',port))
    print("socket binded to %s" %(port))

    s.listen(5)
    print("socket is listening")

    while True: 
 
        # Establish connection with client. 
        c, addr = await s.accept()     
        print ('Got connection from', addr )

        # send a thank you message to the client. encoding to send byte type. 
        c.send('Player(x,y)'.encode()) 
 
        # Close the connection with the client 
        c.close()
   
        # Breaking once connection closed
        break



def connectClient():
   # Create a socket object 
    s = socket.socket()         
 
    # Define the port on which you want to connect 
    port = 12345               
 
    # connect to the server on local computer 
    s.connect(('127.0.0.1', port)) 
 
    # receive data from the server and decoding to get the string.
    print (s.recv(1024).decode())
    # close the connection 
    s.close()     
     