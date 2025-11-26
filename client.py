from socket import *
from threading import Thread
class receive_message:
    def __init__(self, clientSock):
        self.clientSock=clientSock
        Thread(target=self.display, args=()).start()
    def display(self):
        while True:
            try:
                self.msg=self.clientSock.recv(200)
                if self.msg:
                    print("Received:", self.msg.decode())
                else:
                    break
            except:
                break
    
    
serverAdd="127.0.0.1"
serverPort=12000
clientSock= socket(AF_INET, SOCK_STREAM)
clientSock.connect((serverAdd, serverPort))
print("Connected to server! You can now send messages.")
receive_message(clientSock)
while True:
    data= input("write text:")
    clientSock.send(data.encode())

