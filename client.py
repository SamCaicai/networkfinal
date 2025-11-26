from socket import *
from threading import Thread
import sys

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
    
    
# Server configuration - can be set via command line argument
# Usage: python client.py [server_ip] [port]
# Example: python client.py 192.168.1.100 12000
serverAdd = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
serverPort = int(sys.argv[2]) if len(sys.argv) > 2 else 12000
clientSock= socket(AF_INET, SOCK_STREAM)
clientSock.connect((serverAdd, serverPort))
print("Connected to server! You can now send messages.")
receive_message(clientSock)
while True:
    data= input("write text:")
    clientSock.send(data.encode())

