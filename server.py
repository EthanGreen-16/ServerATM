# ETHAN GREEN; 010995145
import socket
import threading
from sqlite3 import connect

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

balance = 100.00

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    global balance


    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT).strip()


            parts = msg.split()
            command = parts[0]

            if command == "DEPOSIT":
                if len(parts) < 2:
                    conn.send("[ERROR] Amount is Required".encode(FORMAT))
                    return

                try:
                    amount = float(parts[1])
                    if amount > 0:
                        balance += amount
                    else:
                        conn.send("[ERROR] Value must be greater than Zero".encode(FORMAT))
                except ValueError:
                    conn.send("[ERROR] Amount must be a Number".encode(FORMAT))




            elif command == "WITHDRAW":
                if len(parts) < 2:
                    conn.send("[ERROR] Amount is Required".encode(FORMAT))

                try:
                    amount = float(parts[1])
                except ValueError:
                    conn.send("[ERROR] Amount must be a Number".encode(FORMAT))
                    return

                if amount < 0:
                    conn.send("[ERROR] Value must be greater than Zero".encode(FORMAT))
                elif amount > balance:
                    conn.send("[ERROR] Cannot Withdraw more than current Balance".encode(FORMAT))
                else:
                    balance -= amount

            elif command == "BALANCE":
                conn.send(f"     Balance: ${balance}".encode(FORMAT))
            elif command == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            print(balance)
            conn.send("\nMSG Received".encode(FORMAT))
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()