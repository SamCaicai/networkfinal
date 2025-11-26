from socket import *
from threading import Thread
import sys

# List to store all connected client sockets
clients = []
clients_lock = []  # Simple lock mechanism using list

def broadcast_message(message, sender_socket):
    """
    Broadcast a message to all connected clients except the sender
    """
    # Create a copy of clients list to avoid modification during iteration
    clients_copy = clients.copy()
    
    for client in clients_copy:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                # If sending fails, client might have disconnected
                if client in clients:
                    clients.remove(client)
                client.close()

def handle_client(client_socket, address):
    """
    Handle communication with a single client
    """
    print(f"Client connected from {address}")
    
    # Add client to the list
    clients.append(client_socket)
    print(f"Total clients connected: {len(clients)}")
    
    try:
        while True:
            # Receive message from client
            message = client_socket.recv(200)
            
            if not message:
                # Client disconnected
                break
            
            # Display received message on server
            print(f"Received from {address}: {message.decode()}")
            
            # Broadcast message to all other clients
            broadcast_message(message, client_socket)
            
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        # Remove client from list and close connection
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()
        print(f"Client {address} disconnected. Total clients: {len(clients)}")

def main():
    # Server configuration
    server_port = 12000  # Default port, can be changed via command line
    
    if len(sys.argv) > 1:
        server_port = int(sys.argv[1])
    
    # Create TCP server socket
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Allow reuse of address
    
    # Bind socket to address and port
    server_socket.bind(('', server_port))
    
    # Start listening for connections
    server_socket.listen(5)
    print(f"Server is listening on port {server_port}")
    print("Waiting for clients to connect...")
    
    try:
        while True:
            # Accept a new client connection
            client_socket, address = server_socket.accept()
            
            # Start a new thread to handle this client
            client_thread = Thread(target=handle_client, args=(client_socket, address))
            client_thread.daemon = True  # Thread will exit when main program exits
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        # Close all client connections
        for client in clients:
            client.close()
        server_socket.close()
        print("Server closed.")

if __name__ == "__main__":
    main()


