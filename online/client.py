import socket, sys
import threading

HOST = '172.20.10.11'  # adresse ip du serveur
PORT = 63678
CODE = 'utf8'



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
msg=""

def send():
    msg = input(":")
    s.send(bytes(msg, CODE))

while msg != b'exit':
    threading.Thread(target=send, daemon=True).start()
    data = s.recv(1024).decode(CODE)
    print(data)

s.close()