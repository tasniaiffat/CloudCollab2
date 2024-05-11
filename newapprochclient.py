import socket
import threading
from tkinter import *

# Client configuration
HOST = 'localhost'
PORT = 5556

# Client initialization
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Function to continuously receive data from the server
def receive_data():
    while True:
        try:
            # Receive data from the server and update the text in the GUI
            data = client.recv(1024).decode('utf-8')
            text.delete('1.0', END)
            text.insert(END, data)
        except:
            break

# Function to send data to the server
def send_data(event=None):
    data = text.get('1.0', END)
    client.send(data.encode('utf-8'))

# GUI setup
root = Tk()
root.title("Collaborative Text Editor")

text = Text(root)
text.pack(expand=True, fill='both')

text.bind("<KeyRelease>", send_data)

# Start receiving data from the server
receive_thread = threading.Thread(target=receive_data)
receive_thread.start()

root.mainloop()
