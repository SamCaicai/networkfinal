from socket import *
from threading import Thread
import sys
class receive_message:
    def __init__(self, clientSock):
        self.clientSock=clientSock
        self.msg= self.clientSock.recv(200)
        print("%d", self.msg)
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
    
#serverAdd="127.0.0.1"
#serverPort= 12000
ip= input('Type in server ip:')

serverAdd=sys.argv[1] if len(sys.argv)>1 else ip
serverPort=int(sys.argv[2]) if len(sys.argv)>2 else 12000
#udp = socket(AF_INET, SOCK_DGRAM)
#udp.bind(("", serverPort))
print("Listening for server broadcasts...")

#serverAdd = None
#while serverAdd is None:
#    data, addr = udp.recvfrom(1024)
    #data, addr= udp.recv(200)
#    msg = data.decode()

#    if msg.startswith("SERVER_IP="):
#        serverAdd = msg.split("=")[1]
#        print("Discovered server at:", serverAdd)

#udp.close()

clientSock= socket(AF_INET, SOCK_STREAM)
clientSock.connect((serverAdd, serverPort))
request_user=clientSock.recv(200)
user=input(request_user).encode()
clientSock.send(user)
print("Connected to server! You can now send messages.")
receive_message(clientSock)
while True:
    data= input("write text:")
    clientSock.send(data.encode())

