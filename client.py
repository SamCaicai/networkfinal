from socket import *
from Threading import Thread
class receive_message:
    def __init__(self, clientSock):
        self.clientSock=clientSock
        self.msg= self.clientSock.recv(200)
        print("%d", self.msg)
        Thread(target=self.display, args=()).start()
    def display(self):
        self.msg=self.clientSock.recv(200)
        print( "%d", self.msg)
    
    
serverAdd="127.0.0.1"
serverPort=
clientSock= socket(AF_INET, SOCK_STREAM)
clientSock.connect(serverAdd, serverPort)
receive_message(clientSock)
while True:
    data= input("write text:")
    clientSock.send(data.encode())

