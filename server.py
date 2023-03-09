import socket
import threading
import pickle
import random

HOST = socket.gethostname(socket.gethostbyname())
PORT = 5050

objects = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

class Account:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.points = 0
        self.ppc = 1
        self.plots = []
#send_data='{}-{}-{}-{}'.format(None, None, None, None).encode()

abin = Account("Albin", "albin123")
avin = Account("Alvin", "alvin123")

accounts = [abin, avin]


def handle(client, address):
    account = None
    while True:
            data=client.recv(1024).decode("utf-8")
            data=data.split('-')
            if data[0] == "Disconnect":
                send_data='{}-{}-{}-{}'.format("Shutdown", None, None, None).encode()
                client.send(send_data)
                break
            if not account == None:
                if data[0] == 'Points':
                    account.points += account.ppc
                if data[0] == "GetPoints":
                    send_data='{}-{}-{}-{}'.format("GetPoints", account.points, None, None).encode()
                    client.send(send_data)
                if data[0] == "Leaderboard":
                    leaderboard = sorted(accounts, key=lambda x: x.points, reverse=True)
                    new = ""
                    for x in leaderboard:
                        new += f"{x.username}: {x.points}\n"
                    send_data='{}-{}-{}-{}'.format("Leaderboard", new, None, None).encode()
                    client.send(send_data)
                if data[0] == "Buy Ppc":
                    if account.points >= 20:
                        account.points -= 20
                        account.ppc += 1
            else:
                if data[0] == "Login":
                    for x in accounts:
                        if x.username == data[1] and x.password == data[2]:
                            account = x
                            send_data='{}-{}-{}-{}'.format("Login", None, None, None).encode()
                            client.send(send_data)
                            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!")
        #broadcast(f"Client {address} connected to the server".encode('utf-8'))
        send_data='{}-{}-{}-{}'.format("Connected", None, None, None).encode()
        client.send(send_data)
        thread = threading.Thread(target=handle, args=(client, address))
        thread.start()

print("Server running...")

receive()
