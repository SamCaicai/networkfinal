"""
Quick test script to verify broadcast functionality
Simulates 3 clients connecting and sending messages
"""
from socket import *
import time
from threading import Thread

def client_simulator(client_id, delay=1):
    """Simulate a client that connects, sends a message, and receives broadcasts"""
    try:
        print(f"\n[Client {client_id}] Connecting...")
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(('127.0.0.1', 12000))
        print(f"[Client {client_id}] Connected!")
        
        # Wait a bit for other clients to connect
        time.sleep(delay)
        
        # Send a message
        message = f"Hello from Client {client_id}!"
        print(f"[Client {client_id}] Sending: {message}")
        sock.send(message.encode())
        
        # Wait and try to receive broadcasts
        time.sleep(2)
        sock.settimeout(0.5)
        received_count = 0
        while received_count < 2:  # Expect messages from 2 other clients
            try:
                data = sock.recv(200)
                if data:
                    print(f"[Client {client_id}] Received: {data.decode()}")
                    received_count += 1
            except:
                break
        
        sock.close()
        print(f"[Client {client_id}] Disconnected\n")
        
    except Exception as e:
        print(f"[Client {client_id}] Error: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Feature 1 - Broadcast Communication")
    print("=" * 50)
    print("\nMake sure server.py is running first!")
    print("Waiting 2 seconds for server to be ready...\n")
    time.sleep(2)
    
    # Start 3 clients with slight delays
    threads = []
    for i in range(1, 4):
        thread = Thread(target=client_simulator, args=(i, i * 0.5))
        thread.start()
        threads.append(thread)
        time.sleep(0.3)
    
    # Wait for all to complete
    for thread in threads:
        thread.join()
    
    print("=" * 50)
    print("Test completed!")
    print("=" * 50)

