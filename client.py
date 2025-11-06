# ETHAN GREEN; 010995145
import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def menu():
    while True:
        print("\n===MENU===")
        print("1. Deposit to Account")
        print("2. Withdraw from Account")
        print("3. Check Account Balance")
        print("4. Exit")


        choice = input(" >> ")

        match choice:
            case "1":
                amount = input("    Deposit Amount: $")
                send(f"DEPOSIT {amount}")
            case "2":
                amount = input("    Withdrawal Amount: $")
                send(f"WITHDRAW {amount}")
            case "3":
                send("BALANCE")
            case "4":
                send(DISCONNECT_MESSAGE)
                break


menu()