import os,sys, time, pickle
import socket
import threading
from getpass import getpass
import codecs

def create_thread(target):
    thread=threading.Thread(target=target)
    thread.daemon=True
    thread.start()

HOST = input("IP: ")
PORT = 5050

connection_established=False
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    sock.connect((HOST,PORT))
    connection_established=True
except :
    pass

running = True

account = None

def receive_data():
    global turn,connection_established, running, account
    while True:
        #try:
            data=sock.recv(1024).decode("utf-8")
            data=data.split('-')
            if data[0] == "GetInfo":
                a = pickle.loads(codecs.decode(data[1].encode(), "base64"))
                input(f"Points: {a[0]}\nPpc: {a[1]}\nPps: {a[2]}\nPPc_u: {a[3]}")
            if data[0] == "Connected":
                input("Connected to server")
            if data[0] == "Login":
                input("Logged in")
            if data[0] == "Shutdown":
                running = False
                break
            if data[0] == "Leaderboard":
                input(data[1])
        #except:
         #   print("ahh")

create_thread(receive_data)

login = False

while running:
    try:
        time.sleep(0.2)
        user_input = input("> ")
        if user_input == "Help":
            input("Login: Login to An Account\nGet: Get Your Points\nBuy: Buys extra Ppc (Cost: 20p) or Pps (Cost: 50p)\n")
        if not login:
            if user_input == "Login":
                send_data='{}-{}-{}-{}'.format("Login", input("Username: "), getpass(), None).encode()
                sock.send(send_data)
                login = True
        else:
            if user_input == "Buy":
                user_input = input("1: Buy Ppc\n2: Buy Pps\n3: Get Cheaper Ppc (RESETS your points and ppc)\n> ")
                if user_input == "1":
                    send_data='{}-{}-{}-{}'.format("Buy Ppc", input("Num > "), None, None).encode()
                    sock.send(send_data)
                if user_input == "2":
                    send_data='{}-{}-{}-{}'.format("Buy Pps", input("Num > "), None, None).encode()
                    sock.send(send_data)
                if user_input == "3":
                    send_data='{}-{}-{}-{}'.format("Get Cheaper Ppc", None, None, None).encode()
                    sock.send(send_data)            
                continue
            elif user_input == "Get":
                send_data='{}-{}-{}-{}'.format("GetInfo", None, None, None).encode()
                sock.send(send_data)
            elif user_input == "Leaderboard":
                send_data='{}-{}-{}-{}'.format("Leaderboard", None, None, None).encode()
                sock.send(send_data)
            else:
                send_data='{}-{}-{}-{}'.format("Points", None, None, None).encode()
                sock.send(send_data)

    except:
        print("ahh")
