<<<<<<< HEAD
import socket
import threading
import tkinter as tk

HOST = '127.0.0.1'
PORT = 65433

class ChatClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.username = None

        # Prompt for the username
        self.prompt_for_username()

        # Start receiving messages
        self.start_receiving()

    def prompt_for_username(self):
        # Make an input prompt window
        prompt_window = tk.Toplevel(root)
        prompt_window.title("Username")
        tk.Label(prompt_window, text="Enter your username:").pack(pady=5)
        username_entry = tk.Entry(prompt_window)
        username_entry.pack(padx=10, pady=5)

        def set_username():
            self.username = username_entry.get()
            prompt_window.destroy()

        tk.Button(prompt_window, text="OK", command=set_username).pack(pady=5)
        root.wait_window(prompt_window)

    def start_receiving(self):
        threading.Thread(target=self.receive).start()

    def receive(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.display_message(message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def send(self, message):
        try:
            self.client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {e}")

    def send_message(self):
        index = chat_text.index(tk.INSERT)
        start_idx = f"{index} linestart"
        end_idx = f"{index} lineend"
        line_text = chat_text.get(start_idx, end_idx)
        if line_text.strip():  # Send only if there's text
            message = f"{start_idx}:{self.username}:{line_text.strip()}"
            self.send(message)

    def on_text_change(self, event):
        self.send_message()

    def display_message(self, message):
        try:
            index, username, content = message.split(':', 2)
            chat_text.config(state=tk.NORMAL)  # Ensure text widget is editable
            chat_text.delete(index + " linestart", index + " lineend")
            chat_text.insert(index, content)
            chat_text.see(tk.INSERT)  # Optional: Adjust view to the insertion cursor
            chat_text.config(state=tk.NORMAL)  # Set state back to NORMAL to allow editing
        except Exception as e:
            print(f"Error displaying message: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chat Client")

    chat_text = tk.Text(root, wrap=tk.WORD, width=50, height=20)
    chat_text.pack(padx=10, pady=10)
    chat_text.config(state=tk.NORMAL)  # Start with text widget being editable

    chat_client = ChatClient(HOST, PORT)
    chat_text.bind("<KeyRelease>", chat_client.on_text_change)

    root.mainloop()
=======
import socket 
import tqdm

BUFFER_SIZE = 4096 
host = 'localhost'
FORMAT = 'utf-8'
port = 7071

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"[+] Connecting to {host} : {port}")
client_socket.connect((host,port))
print("[+] Connected.")

arr = []

file_recv = client_socket.recv(1024).decode()
arr.append(file_recv)
print(f"{file_recv}")

selected_file = input("Which file do you want to download? -> ") 
client_socket.send(selected_file.encode(FORMAT))

file_size = int(client_socket.recv(1024).decode())
print(f"File size: {file_size} bytes")

name = "file.pdf"
file = open(name, "wb")

progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=file_size)

while True:
    data = client_socket.recv(BUFFER_SIZE)
    if not data or data.endswith(b"<END>"):
        break
    file.write(data)
    progress.update(len(data))

file.close()
print("File received successfully.")

client_socket.close()
>>>>>>> dabca38f2f6e7c34fe0ea640eac416764d46c509
