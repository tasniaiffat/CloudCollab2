import socket
import threading
import os

HOST = 'localhost'
PORT = 7071
SIZE = 1024
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

def handle_client(conn,address):
    print(f"[NEW CONNECTION] Connected to {address}")
    send_data = ''
    connected=True
    # while connected:
    arr=os.listdir("D:\\CP")
    # conn.send(str(len(arr)).encode(FORMAT))
    
    for ob in arr:
        ob=ob+"\n"
        send_data = send_data+ob
        # conn.send(ob.encode())
    conn.send(send_data.encode(FORMAT))

    filename = conn.recv(SIZE).decode()
    # print(filename)
    print(filename)
    
    if filename == "quit": 
        connected = False
        # break
    filename = "D:\\CP\\" + filename  
    # filename = "Introduction to Algorithms - Corman.pdf"
    filesize = os.path.getsize(filename)
    
    conn.send(str(filesize).encode(FORMAT))
    
    file=open(filename,"rb")
    data=file.read()
    file.close()
    # data = data + b"<END>"
    # print(data)
    data = data + b"<END>"
    conn.sendall(data)
            
        
    conn.close()

def start():
    while True:
        server.listen()
        print(f"[LISTENING] Server is listening on {HOST}:{PORT}")    
        while True:
            client_conn, address = server.accept()
            thread = threading.Thread(target=handle_client, args=(client_conn, address))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] Server is starting...")
start()

    
    