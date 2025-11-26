"""
Simple test script to verify the server is working
This creates multiple test clients to test broadcast functionality
"""
from socket import *
import time
from threading import Thread

def test_client(client_id, port=12000):
    """Simulate a client connection"""
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(('127.0.0.1', port))
        print(f"Client {client_id} connected")
        
        # Send a test message
        message = f"Hello from Client {client_id}"
        client_socket.send(message.encode())
        print(f"Client {client_id} sent: {message}")
        
        # Wait to receive broadcast messages
        time.sleep(2)
        
        # Try to receive messages
        try:
            client_socket.settimeout(1)
            while True:
                data = client_socket.recv(200)
                if data:
                    print(f"Client {client_id} received: {data.decode()}")
        except:
            pass
        
        client_socket.close()
        print(f"Client {client_id} disconnected")
        
    except Exception as e:
        print(f"Client {client_id} error: {e}")

if __name__ == "__main__":
    print("Starting test clients...")
    print("Make sure the server is running on port 12000")
    
    # Create 3 test clients
    threads = []
    for i in range(1, 4):
        thread = Thread(target=test_client, args=(i,))
        thread.start()
        threads.append(thread)
        time.sleep(0.5)  # Stagger connections
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print("Test completed")


