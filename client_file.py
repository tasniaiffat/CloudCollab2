import socket 
import tqdm
import os

BUFFER_SIZE = 4096 
host = 'localhost'
FORMAT = 'utf-8'
port = 7071


def file_download(client_socket):

    arr = []

    file_recv = client_socket.recv(1024).decode()
    arr.append(file_recv)
    print(f"{file_recv}")

    selected_file = input("Which file do you want to download? -> ") 
    client_socket.send(selected_file.encode(FORMAT))

    # file_size = client_socket.recv(1024).decode()
    # print(f"File size: {file_size} bytes")

    name = "file.pdf"
    # file = open(name, "wb")

    # progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=float(file_size))
    
    sz = client_socket.recv(1024).decode()
    print(sz)
    sz = int(sz)
    client_socket.send("sz".encode())
    file = open(name, "wb")

    current_packet = 0
    while True:
        if current_packet == sz:
            break
        try:
            file_data = client_socket.recv(1024)
            if not file_data:
                break
            file.write(file_data)
            client_socket.send("ACK".encode())  # sending ACK for each packet received
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
    client_socket.close()

def file_upload(client_socket) : 

    filename = input("Which file do you want to upload?")
    # client_socket.send(filename.encode(FORMAT))
    # filename = ".\\" + filename
    filesize = os.path.getsize(filename)
    print(filesize)
    # client_socket.send(filesize.encode(FORMAT))

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
    client_socket.send(f"{total_packets}".encode())
    # print(basename)
    ackk = client_socket.recv(1024).decode()
    if ackk == "sz":
        while current_packet < total_packets:
            for i in range(total_packets):
                client_socket.send(packets[i])
                # print(packets[i])
                try:
                    ack = client_socket.recv(1024).decode()
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

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"[+] Connecting to {host} : {port}")
client_socket.connect((host,port))
print("[+] Connected.")

option = input("Do you want to download or upload file?")

client_socket.send(option.encode(FORMAT))

if option == "download":
    file_download(client_socket)
else :
    file_upload(client_socket)    

