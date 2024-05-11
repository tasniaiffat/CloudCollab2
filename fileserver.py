import socket
import threading
import os
import tqdm
import time

HOST = 'localhost'
PORT = 7071
SIZE = 1024
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

def file_download(conn):

    arr = []

    arr=os.listdir(".\\Server")
    # conn.send(str(len(arr)).encode(FORMAT))
    send_data = ""

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
    filename = ".\\Server\\" + filename  

    filesize = os.path.getsize(filename)
    print(filesize)
    # conn.send(str(filesize).encode())
    
    ### Send with implemented TCP Flow Control and TCP Conjestion control


    seq_num = 0
    cwnd = 1
    ssthresh = 1024
    rtt = 1
    # ack = conn.recv(1024).decode()

    file = open(filename, "rb")
    window_size = 4  # set the window size to 4
    packets = []
    current_packet = 0
    total_packets = (filesize // 1024) + 1
    
    print(total_packets)

    for i in range(total_packets):
        file_data = file.read(1024)
        packets.append(file_data)
    conn.send(f"{total_packets}".encode())
    # print(basename)
    ackk = conn.recv(1024).decode()
    if ackk == "sz":
        while current_packet < total_packets:
            for i in range(total_packets):
                conn.send(packets[i])
                print(packets[i])
                try:
                    ack = conn.recv(1024).decode()
                    if ack == "ACK":
                        current_packet += 1
                        if seq_num == len(file_data):
                            # All packets have been acknowledged
                            break
                        if cwnd < ssthresh:
                            cwnd *= 2
                        else:
                            cwnd += 1
                    print(cwnd)
                    print(f"Packet {current_packet} acknowledged.")
                except:
                    ssthresh=max(cwnd/2,1)
                    cwnd=1

                    continue
    else:
        print('sz not rcvd')
    file.close()

    print(f" Total {current_packet} Packet acknowledged.")
    print("Data has been transmitted successfully...")
    # send_btn.destroy()
    # Label(window, text=f'Data has been transmitted successfully...', font=('Acumin Variable Concept', 13,),
        #   bg='#7FFFD4', fg="#000").place(
        # x=90, y=350)
        
    # conn.close()

def file_upload(conn):
    
    # filename = conn.recv(1024).decode()
    # print(filename)
    # filesize = os.path.getsize(filename)
    # file_size = conn.recv(1024).decode("utf-8")
    # print(file_size)
    name = ".\\Server\\new_file.pdf"
    file = open(name, "wb")

    sz = conn.recv(1024).decode()
    print(sz)
    sz = int(sz)
    conn.send("sz".encode())
    file = open(name, "wb")

    current_packet = 0
    while True:
        if current_packet == sz:
            break
        try:
            file_data = conn.recv(1024)
            if not file_data:
                break
            file.write(file_data)
            conn.send("ACK".encode())  # sending ACK for each packet received
            current_packet += 1
            print(f"Packet {current_packet} received.")
        except:
            continue
    file.close()

    print(f"Total {current_packet} Packet  received.")
    print("file has been received successfully..")
    # rr.destroy()
    # Label(main, text=f'File has been received successfully.....', font=('Acumin Variable Concept', 13,),
    #         bg='#7FFFD4', fg="#000").place(x=90, y=360)

    print("File received successfully.")
    conn.close()


def handle_client(conn,address):
    print(f"[NEW CONNECTION] Connected to {address}")
    time.sleep(2)
    option = conn.recv(1024).decode()
    # print(option)
    if option == "download":
        file_download(conn) 
    else :
        file_upload(conn)           
        
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

    
    