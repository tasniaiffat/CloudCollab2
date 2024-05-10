import socket
import threading

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65433        # Port to listen on

clients = []

def handle_client(client_socket, addr):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Received message from {addr}: {data}")
            broadcast(data)
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            break

    clients.remove(client_socket)
    client_socket.close()

def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error broadcasting message to a client: {e}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server is listening on {HOST}:{PORT}")
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connected to {addr}")
            clients.append(client_socket)
            threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    start_server()
