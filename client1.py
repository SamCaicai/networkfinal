import socket
from threading import Thread
import sys

BUFFER_SIZE = 1024
DEFAULT_PORT = 12000


class MessageReceiver:
    def __init__(self, client_sock: socket.socket):
        self.client_sock = client_sock
        self._running = True
        self.thread = Thread(target=self._display_loop, daemon=True)
        self.thread.start()

    def _display_loop(self):
        while self._running:
            try:
                data = self.client_sock.recv(BUFFER_SIZE)
                if not data:
                    print("\n[Disconnected from server]")
                    break
                print("\n" + data.decode())
                # Reprint prompt after incoming message so user sees it
                print("write text (or /quit): ", end="", flush=True)
            except (ConnectionResetError, ConnectionAbortedError, OSError) as e:
                print(f"\n[Connection error: {e}]")
                break
            except Exception as e:
                print(f"\n[Unexpected error in receiver: {e}]")
                break

        self._running = False


def main():
    # Get server IP (CLI arg overrides input)
    ip = input("Type in server IP (or leave blank for 127.0.0.1): ").strip()
    if not ip:
        ip = "127.0.0.1"

    server_addr = sys.argv[1] if len(sys.argv) > 1 else ip
    server_port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT

    # Create socket and connect
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_sock.connect((server_addr, server_port))
    except Exception as e:
        print(f"Could not connect to {server_addr}:{server_port} -> {e}")
        return

    # Receive username prompt from server
    try:
        request_user = client_sock.recv(BUFFER_SIZE)
        if not request_user:
            print("Server closed connection before sending username prompt.")
            client_sock.close()
            return

        prompt = request_user.decode()
        username = input(prompt + " ").strip()
        if not username:
            username = "Anonymous"

        client_sock.sendall(username.encode())
    except Exception as e:
        print(f"Error during username exchange: {e}")
        client_sock.close()
        return

    print("Connected to server! You can now send messages.")
    receiver = MessageReceiver(client_sock)

    # Main send loop
    try:
        while True:
            msg = input("write text (or /quit): ").strip()
            if msg.lower() in ("/quit", "/exit"):
                print("Closing connection...")
                break
            if not msg:
                continue
            try:
                client_sock.sendall(msg.encode())
            except (BrokenPipeError, ConnectionResetError, OSError) as e:
                print(f"[Send error: {e}]")
                break
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
    finally:
        client_sock.close()


if __name__ == "__main__":
    main()

