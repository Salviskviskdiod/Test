import os,sys, time, pickle
import socket
import threading
from getpass import getpass
import codecs, math

def create_thread(target):
    thread=threading.Thread(target=target)
    thread.daemon=True
    thread.start()

HOST = f"{input('Num: ')}.tcp.eu.ngrok.io"
PORT = int(input("PORT: "))

connection_established=False
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    sock.connect((HOST,PORT))
    connection_established=True
except :
    pass

running = True

account = None

class Account:
    def __init__(self):
        self.points = None
        self.ppc = None
        self.pps = None
        self.dict = {0 : "points", 1 : "ppc", 2: "pps"}

def receive_data():
    global turn,connection_established, running, account
    while True:
        #try:
            data=sock.recv(1024).decode("utf-8")
            data=data.split('-')
            if data[0] == "Connected":
                input("Connected to server")
            if data[0] == "Login":
                input("Logged in")
            if data[0] == "Shutdown":
                running = False
                break
            if data[0] == "Leaderboard":
                input(data[1])
            if data[0] == "Info":
                a = pickle.loads(codecs.decode(data[1].encode(), "base64"))
                account = Account()
                for i, x in enumerate(a):
                    setattr(account, account.dict[i], int(x))
        #except:
         #   print("ahh")

create_thread(receive_data)

login = False

while running:
    try:
        time.sleep(0.2)
        user_input = input("> ")
        if user_input == "Help":
            input("Login: Login to An Account\nGet: Get Your Points\nBuy: Buy more Ppc (Cost: 20p) or Pps (Cost: 50p)\n")
        if not login:
            if user_input == "Login":
                send_data='{}-{}-{}-{}'.format("Login", input("Username: "), getpass(), None).encode()
                sock.send(send_data)
                login = True
        else:
            if user_input == "Buy":
                user_input = input("1: Buy Ppc\n2: Buy Pps\n> ")
                if user_input == "1":
                    i = math.floor(account.points / 20)
                    send_data='{}-{}-{}-{}'.format("Buy Ppc", input(f"Num (Max: {i}): "), None, None).encode()
                    sock.send(send_data)
                if user_input == "2":
                    i = math.floor(account.points / 50)
                    send_data='{}-{}-{}-{}'.format("Buy Pps", input(f"Num (Max: {i}): "), None, None).encode()
                    sock.send(send_data)           
                continue
            elif user_input == "Get":
                if not account == None:
                    input(f"Points: {account.points}\nPpc: {account.ppc}\nPps: {account.pps}")
            elif user_input == "Leaderboard":
                send_data='{}-{}-{}-{}'.format("Leaderboard", None, None, None).encode()
                sock.send(send_data)
            else:
                send_data='{}-{}-{}-{}'.format("Points", None, None, None).encode()
                sock.send(send_data)

    except:
        print("ahh")
