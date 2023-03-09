import os,sys
import socket
import threading

def create_thread(target):
    thread=threading.Thread(target=target)
    thread.daemon=True
    thread.start()


HOST = '10.11.29.81'
PORT = 5050

connection_established=False
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    sock.connect((HOST,PORT))
    connection_established=True
except :
    pass

running = True

def receive_data():
    global turn,connection_established, running
    while True:
        #try:
            data=sock.recv(1024).decode("utf-8")
            data=data.split('-')
            if data[0] == "GetPoints":
                input(data[1])  
            if data[0] == "Connected":
                input("Connected to server")
            if data[0] == "Login":
                input("Logged in")
            if data[0] == "Shutdown":
                running = False
                break
            if data[0] == "Leaderboard":
                input(data[1])

create_thread(receive_data)

while running:
    os.system("cls")
    user_input = input("> ")
    if user_input == "Login":
        send_data='{}-{}-{}-{}'.format("Login", input("Username: "), input("Password: "), None).encode()
        sock.send(send_data)
    if user_input == "Buy":
        send_data='{}-{}-{}-{}'.format("Buy Ppc", None, None, None).encode()
        sock.send(send_data)
    if user_input == "Get":
        send_data='{}-{}-{}-{}'.format("GetPoints", None, None, None).encode()
        sock.send(send_data)
    else:
        send_data='{}-{}-{}-{}'.format("Points", None, None, None).encode()
        sock.send(send_data)
