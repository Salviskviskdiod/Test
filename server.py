import socket
import threading, time
import pickle
import random
import codecs

HOST = "localhost"
PORT = 9999

accounts = []

class Account:
    def __init__(self, username: str, password: str):
        self.online = False
        self.username = username
        self.password = password
        self.points = 0
        self.ppc = 1
        self.pps = 0
        self.client = None
        accounts.append(self)
class Item:
    def __init__(self, name, ppc):
        self.name = name
        self.ppc = ppc
banana = Item(1.3)
#if input("Load Y / N > ").lower() == "y":
   # with open("save.txt", "r") as f:
   #     accounts = pickle.loads(codecs.decode(f.read().encode(), "base64"))
    #    print(accounts.points)
     #   for x in accounts:
       #     print(x.__dict__)
#else:


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

def sec1():
    global accounts
    while True:
        time.sleep(1)
      #  with open("save.txt", "w") as f:
       #     new = []
       #     for i, account in enumerate(accounts):
       #         a = globals()[f"Obj{i}"]= Account(account.username, account.password)
       #         for x in account.__dict__:
          #          setattr(a, x, getattr(account, x))
       #         a.client = None
            #    new.append(a)
            #f.write(codecs.encode(pickle.dumps(new), "base64").decode())
        for account in accounts:
            if account.online:
                send_data='{}-{}-{}-{}'.format("Info", codecs.encode(pickle.dumps([account.points, account.ppc, account.pps]), "base64").decode(), None, None).encode()
                account.client.send(send_data)
            account.points += account.pps

sec1_thread = threading.Thread(target=sec1)
sec1_thread.start()



def handle(client, address):
    account = None
    while True:
        try:
            data=client.recv(1024).decode("utf-8")
            data=data.split('-')
            if data[0] == "Disconnect":
                account.online = False
                send_data='{}-{}-{}-{}'.format("Shutdown", None, None, None).encode()
                client.send(send_data)
                break
            if not account == None:
                if data[0] == 'Points':
                    account.points += account.ppc
                if data[0] == "GetInfo":
                    send_data='{}-{}-{}-{}'.format("GetInfo", codecs.encode(pickle.dumps([account.points, account.ppc, account.pps]), "base64").decode(), None, None).encode()
                    client.send(send_data)
                if data[0] == "Leaderboard":
                    leaderboard = sorted(accounts, key=lambda x: x.points, reverse=True)
                    new = ""
                    for x in leaderboard:
                        new += f"{x.username}: Points: {x.points}    Ppc: {x.ppc}    PPs: {x.pps}\n"
                    send_data='{}-{}-{}-{}'.format("Leaderboard", new, None, None).encode()
                    client.send(send_data)
                if data[0] == "Buy Ppc":
                    if account.points >= 20 * int(data[1]):
                        account.points -= 20 * int(data[1])
                        account.ppc += int(data[1])
                if data[0] == "Buy Pps":
                    if account.points >= 50 * int(data[1]):
                        account.points -= 50 * int(data[1])
                        account.pps += int(data[1])
            else:
                if data[0] == "Login":
                    for x in accounts:
                        if x.username == data[1] and x.password == data[2]:
                            account = x
                            account.online = True
                            account.client = client
                            send_data='{}-{}-{}-{}'.format("Login", None, None, None).encode()
                            client.send(send_data)
                            print(f"Client {address} Logged into account {account.username}")
                            break
        except:
            print(f"Client {address} {'Account: None' if account == None else f'Account: {account.username}'} disconnected")
            if not account == None:
                account.online = False
            client.close()
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

print(f"Server running on {HOST}")

receive()
