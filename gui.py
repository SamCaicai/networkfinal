import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

BUFFER_SIZE = 1024
DEFAULT_PORT = 12000


class ChatClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")

        self.sock = None
        self.receive_thread = None
        self.connected = False

        self._build_ui()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------------- UI SETUP ---------------- #
    def _build_ui(self):
        # Top frame: connection info
        top_frame = tk.Frame(self.root)
        top_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(top_frame, text="Server IP:").grid(row=0, column=0, sticky="e")
        self.entry_host = tk.Entry(top_frame, width=15)
        self.entry_host.grid(row=0, column=1, padx=5)
        self.entry_host.insert(0, "127.0.0.1")

        tk.Label(top_frame, text="Port:").grid(row=0, column=2, sticky="e")
        self.entry_port = tk.Entry(top_frame, width=6)
        self.entry_port.grid(row=0, column=3, padx=5)
        self.entry_port.insert(0, str(DEFAULT_PORT))

        self.btn_connect = tk.Button(top_frame, text="Connect", command=self.connect_to_server)
        self.btn_connect.grid(row=0, column=4, padx=5)

        # Username frame
        user_frame = tk.Frame(self.root)
        user_frame.pack(padx=10, pady=(0, 5), fill="x")

        tk.Label(user_frame, text="Username:").grid(row=0, column=0, sticky="e")
        self.entry_username = tk.Entry(user_frame, width=15)
        self.entry_username.grid(row=0, column=1, padx=5)

        self.btn_send_username = tk.Button(user_frame, text="Send Username", command=self.send_username, state="disabled")
        self.btn_send_username.grid(row=0, column=2, padx=5)

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(self.root, state="disabled", wrap="word", height=15)
        self.chat_display.pack(padx=10, pady=5, fill="both", expand=True)

        # Bottom frame: message input
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(bottom_frame, text="Message:").grid(row=0, column=0, sticky="e")
        self.entry_message = tk.Entry(bottom_frame)
        self.entry_message.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        self.entry_message.bind("<Return>", self.send_message_event)

        self.btn_send = tk.Button(bottom_frame, text="Send", command=self.send_message, state="disabled")
        self.btn_send.grid(row=0, column=2, padx=5)

        bottom_frame.columnconfigure(1, weight=1)

    # ------------- NETWORKING ------------- #
    def connect_to_server(self):
        if self.connected:
            return

        host = self.entry_host.get().strip() or "127.0.0.1"
        port_str = self.entry_port.get().strip() or str(DEFAULT_PORT)

        try:
            port = int(port_str)
        except ValueError:
            messagebox.showerror("Error", "Port must be an integer.")
            return

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((host, port))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to {host}:{port}\n{e}")
            self.sock.close()
            self.sock = None
            return

        # Receive the server's username prompt (one-time)
        try:
            prompt = self.sock.recv(BUFFER_SIZE)
            if not prompt:
                messagebox.showerror("Error", "Server closed the connection.")
                self.sock.close()
                self.sock = None
                return
            prompt_text = prompt.decode(errors="ignore")
            self.append_chat(prompt_text)
        except Exception as e:
            messagebox.showerror("Error", f"Error receiving username prompt:\n{e}")
            self.sock.close()
            self.sock = None
            return

        self.connected = True
        self.btn_connect.config(state="disabled")
        self.btn_send_username.config(state="normal")
        self.append_chat("[Connected] Please enter your username above and click 'Send Username'.")

    def send_username(self):
        if not self.connected or not self.sock:
            return

        username = self.entry_username.get().strip()
        if not username:
            messagebox.showwarning("Username", "Please enter a username.")
            return

        try:
            self.sock.sendall(username.encode())
        except Exception as e:
            messagebox.showerror("Error", f"Error sending username:\n{e}")
            self.cleanup_socket()
            return

        self.append_chat(f"[You] Username sent: {username}")
        self.btn_send_username.config(state="disabled")
        self.btn_send.config(state="normal")

        # Start background receive thread
        self.receive_thread = threading.Thread(target=self.receive_loop, daemon=True)
        self.receive_thread.start()

    def receive_loop(self):
        while self.connected and self.sock:
            try:
                data = self.sock.recv(BUFFER_SIZE)
                if not data:
                    self.append_chat("[Disconnected from server]")
                    break
                text = data.decode(errors="ignore")
                self.append_chat(text)
            except OSError:
                # Socket likely closed
                break
            except Exception as e:
                self.append_chat(f"[Receive error] {e}")
                break

        self.cleanup_socket()

    # ------------- SENDING MESSAGES ------------- #
    def send_message_event(self, event):
        self.send_message()

    def send_message(self):
        if not self.connected or not self.sock:
            return

        msg = self.entry_message.get().strip()
        if not msg:
            return

        # Allow quit via command
        if msg.lower() in ("/quit", "/exit"):
            self.append_chat("[You] /quit")
            self.cleanup_socket()
            return

        try:
            self.sock.sendall(msg.encode())
        except Exception as e:
            self.append_chat(f"[Send error] {e}")
            self.cleanup_socket()
            return

        # Optional: show your own message in the chat (server may also echo/broadcast it)
        # self.append_chat(f"[You]: {msg}")

        self.entry_message.delete(0, tk.END)

    # ------------- UTILITIES ------------- #
    def append_chat(self, text: str):
        """Append text to the chat display from GUI thread."""
        # Ensure this runs on the Tkinter main thread
        if self.root and threading.current_thread() is not threading.main_thread():
            self.root.after(0, self.append_chat, text)
            return

        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, text + "\n")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

    def cleanup_socket(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
        self.sock = None
        self.connected = False
        self.btn_connect.config(state="normal")
        self.btn_send_username.config(state="disabled")
        self.btn_send.config(state="disabled")

    def on_close(self):
        self.cleanup_socket()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClientGUI(root)
    root.mainloop()
