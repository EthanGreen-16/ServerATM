# ETHAN GREEN; 010995145
import socket
import threading

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


def recv_exact(conn, n):
    data = bytearray()
    while len(data) < n:
        chunk = conn.recv(n - len(data))
        if not chunk:
            return b''
        data.extend(chunk)
    return bytes(data)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    global balance

    while True:
        header = recv_exact(conn, HEADER)
        if not header:
            break

        header_str = header.decode(FORMAT).strip()
        if not header_str.isdigit():
            conn.sendall(b"[ERROR] Bad header\n")
            continue

        msg_len = int(header_str)
        payload = recv_exact(conn, msg_len)
        if msg_len and not payload:
            break

        msg = (payload.decode(FORMAT) if payload else "").strip()
        if not msg:
            conn.sendall(b"[ERROR] Empty command\n")
            continue

        parts = msg.split()
        command = parts[0].upper()

        if command == DISCONNECT_MESSAGE or command == "DISCONNECT":
            conn.sendall(b"[OK] Disconnected\n")
            break

        if command == "DEPOSIT":
            if len(parts) < 2:
                conn.sendall(b"[ERROR] Amount is Required\n")
                continue
            try:
                amount = float(parts[1])
                if amount <= 0:
                    conn.sendall(b"[ERROR] Value must be greater than Zero\n")
                    continue
                balance += amount
                conn.sendall(f"[OK] Deposited ${amount:.2f}. Balance: ${balance:.2f}\n".encode(FORMAT))
            except ValueError:
                conn.sendall(b"[ERROR] Amount must be a Number\n")

        elif command == "WITHDRAW":
            if len(parts) < 2:
                conn.sendall(b"[ERROR] Amount is Required\n")
                continue
            try:
                amount = float(parts[1])
                if amount <= 0:
                    conn.sendall(b"[ERROR] Value must be greater than Zero\n")
                elif amount > balance:
                    conn.sendall(b"[ERROR] Cannot Withdraw more than current Balance\n")
                else:
                    balance -= amount
                    conn.sendall(f"[OK] Withdrew ${amount:.2f}. Balance: ${balance:.2f}\n".encode(FORMAT))
            except ValueError:
                conn.sendall(b"[ERROR] Amount must be a Number\n")

        elif command == "BALANCE":
            conn.sendall(f"Balance: ${balance:.2f}\n".encode(FORMAT))

        else:
            conn.sendall(b"[ERROR] Unknown command\n")

    try:
        conn.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass
    conn.close()
    print(f"[DISCONNECT] {addr} closed.")


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


print("[STARTING] server is starting...")
start()
