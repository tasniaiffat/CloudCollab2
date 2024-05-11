import os
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('localhost', 8000))

file = open("Introduction to Algorithms - Corman.pdf", "rb")

file_size = os.path.getsize("Introduction to Algorithms - Corman.pdf")

client.send("new.pdf".encode())
client.send(str(file_size).encode())

data = file.read()
client.sendall(data)
client.send(b"<END>")

file.close()
client.close()
