from socket import *
from threading import Thread
import sys
import time

# ============================================================================
# FEATURE 1: BROADCAST COMMUNICATION
# ============================================================================
# List to store all connected client sockets for broadcast feature
clients = []

def broadcast_message(message, sender_socket):
    """
    FEATURE 1: Broadcast a message to all connected clients except the sender
    This implements the broadcast functionality where one client's message
    is sent to all other connected clients.
    """
    # Create a copy of clients list to avoid modification during iteration
    clients_copy = clients.copy()
    
    # Send message to all clients except the sender
    for client in clients_copy:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                # If sending fails, client might have disconnected
                if client in clients:
                    clients.remove(client)
                client.close()

# ============================================================================
# FEATURE 2: ONE-TO-ONE PRIVATE MESSAGING
# ============================================================================
# Dictionary to store username-socket pairs for private messaging
# Format: {username: socket}
client_dict = {}

def send_private_message(target_username, message, sender_socket):
    """
    FEATURE 2: Send a private message to a specific target user
    This implements one-to-one messaging where messages are delivered
    only to the intended recipient.
    """
    # Check if target username exists in the dictionary
    if target_username in client_dict:
        try:
            # Send message only to the target client
            client_dict[target_username].send(message)
            return True
        except Exception as e:
            print(f"Error sending to {target_username}: {e}")
            return False
    else:
        return False

def handle_client(client_socket, address, username):
    """
    Handle communication with a single client
    Supports both Feature 1 (broadcast) and Feature 2 (one-to-one messaging)
    Username is passed from the main loop where registration happens
    """
    print(f"Client {username} ({address}) handler started")
    
    # ========================================================================
    # Main message handling loop - supports both features
    # ========================================================================
    try:
        while True:
            # Receive message from client
            message = client_socket.recv(200)
            
            if not message:
                # Client disconnected
                break
            
            message_str = message.decode()
            print(f"Received from {username} ({address}): {message_str}")
            
            # ================================================================
            # FEATURE 2: Check if message is a private message (@username)
            # ================================================================
            if message_str.startswith('@'):
                # Extract target username and message text
                parts = message_str[1:].split(' ', 1)  # Split after @
                
                if len(parts) >= 2:
                    target_username = parts[0]
                    private_message = parts[1]
                    
                    # Format private message with sender info
                    formatted_message = f"[Private from {username}]: {private_message}".encode()
                    
                    # Send private message to target user
                    if send_private_message(target_username, formatted_message, client_socket):
                        # Confirm to sender
                        confirmation = f"Message sent to {target_username}".encode()
                        client_socket.send(confirmation)
                    else:
                        # Inform sender that target user was not found
                        error_msg = f"User '{target_username}' not found. Available users: {', '.join(client_dict.keys())}".encode()
                        client_socket.send(error_msg)
                else:
                    # Invalid format - inform sender
                    error_msg = b"Invalid format. Use: @username message"
                    client_socket.send(error_msg)
            
            # ================================================================
            # FEATURE 1: Broadcast message to all clients (default behavior)
            # ================================================================
            else:
                # Format broadcast message with sender info
                broadcast_msg = f"[{username}]: {message_str}".encode()
                # Broadcast to all other clients
                broadcast_message(broadcast_msg, client_socket)
            
    except Exception as e:
        print(f"Error handling client {username} ({address}): {e}")
    finally:
        # ====================================================================
        # Cleanup when client disconnects
        # ====================================================================
        # Remove from broadcast list (FEATURE 1)
        if client_socket in clients:
            clients.remove(client_socket)
        
        # Remove from username dictionary (FEATURE 2)
        if username in client_dict:
            del client_dict[username]
            # Notify other clients about user leaving
            notification = f"{username} left the chat".encode()
            broadcast_message(notification, None)
        
        client_socket.close()
        print(f"Client {username} ({address}) disconnected. Total clients: {len(clients)}")

# ============================================================================
# TCP Broadcast Server (for server discovery)
# ============================================================================
def tcp_broadcast_server(server_ip, brod_port):
    """
    TCP server that sends server IP address to connecting clients in a separate thread
    This is a helper service for clients to discover the server IP
    """
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    
    try:
        tcp_socket.bind(('', brod_port))
        tcp_socket.listen(5)
        print(f"TCP broadcast server listening on port {brod_port}")
        
        while True:
            try:
                client_socket, address = tcp_socket.accept()
                # Send server IP information to the client
                message = f"Server IP: {server_ip}".encode()
                client_socket.send(message)
                client_socket.close()
            except Exception as e:
                print(f"TCP broadcast error: {e}")
                break
    except Exception as e:
        print(f"TCP broadcast server error: {e}")
    finally:
        tcp_socket.close()

# ============================================================================
# MAIN SERVER FUNCTION
# ============================================================================
def main():
    """
    Main server function that sets up and runs both features simultaneously
    """
    # Server configuration
    server_port = 12000  # Default port, can be changed via command line
    brod_port = 12001   # Port for server discovery
    
    if len(sys.argv) > 1:
        server_port = int(sys.argv[1])
    
    # Get and display server IP address
    server_ip = gethostbyname(gethostname())
    print(f"Server IP: {server_ip}")
    print("=" * 60)
    print("Server starting with both features enabled:")
    print("  FEATURE 1: Broadcast Communication")
    print("  FEATURE 2: One-to-One Private Messaging")
    print("=" * 60)
    
    # Start TCP broadcast server in a separate thread (for server discovery)
    #tcp_broadcast_thread = Thread(target=tcp_broadcast_server, args=(server_ip, brod_port))
    #tcp_broadcast_thread.daemon = True  # Thread will exit when main program exits
    #tcp_broadcast_thread.start()
    
    # ========================================================================
    # FEATURE 1 & 2: Create TCP server socket for main chat functionality
    # ========================================================================
    # Create TCP server socket
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Allow reuse of address
    
    # Bind socket to address and port
    server_socket.bind(('', server_port))
    
    # Start listening for connections
    server_socket.listen(5)
    print(f"Server is listening on port {server_port}")
    print("Waiting for clients to connect...")
    print("\nUsage:")
    print("  - Type message normally to broadcast to all clients (Feature 1)")
    print("  - Type @username message to send private message (Feature 2)")
    print("=" * 60)
    
    try:
        while True:
            # Accept a new client connection
            client_socket, address = server_socket.accept()
            print(f"Client connected from {address}")
            
            # ========================================================================
            # FEATURE 2: Request and receive username from client (in main loop)
            # ========================================================================
            try:
                # Request username from client
                client_socket.send(b"Please enter your username:")
                username = client_socket.recv(200).decode().strip()
                
                # Validate username
                if not username or username in client_dict:
                    if username in client_dict:
                        client_socket.send(b"Username already taken. Connection closed.")
                        client_socket.close()
                        continue
                    username = f"User_{address[0]}"
                
                # Add username-socket pair to dictionary (FEATURE 2)
                client_dict[username] = client_socket
                print(f"Client {address} registered as: {username}")
                
                # Send confirmation to client
                client_socket.send(f"Welcome {username}! You can now send messages.".encode())
                
                # Add client to broadcast list (FEATURE 1)
                clients.append(client_socket)
                print(f"Total clients connected: {len(clients)}")
                
                # Notify other clients about new user (optional)
                notification = f"{username} joined the chat".encode()
                broadcast_message(notification, client_socket)
                
            except Exception as e:
                print(f"Error during username registration: {e}")
                client_socket.close()
                continue
            
            # Start a new thread to handle this client
            # This thread will handle both broadcast and private messaging
            # Username is passed to the handler function
            client_thread = Thread(target=handle_client, args=(client_socket, address, username))
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
