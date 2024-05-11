import socket
import threading

# Server configuration
HOST = 'localhost'
PORT = 5556

# Dictionary to hold connected clients and their text
clients = {}

# Server initialization
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Function to handle client connections
def handle_client(client_socket):
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')
            # Broadcast the received data to all clients except the sender
            for socket in clients:
                if socket != client_socket:
                    socket.send(data.encode('utf-8'))
        except:
            # If an error occurs, remove the client from the list and close the connection
            clients.pop(client_socket)
            client_socket.close()
            break

# Function to accept incoming connections
def accept_connections():
    while True:
        client_socket, _ = server.accept()
        # Add the new client to the dictionary
        clients[client_socket] = True
        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# Start accepting connections
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()
