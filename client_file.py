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
