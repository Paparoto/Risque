# Le serveur attend la connexion d'un client, pour entamer un dialogue avec lui
import socket
import threading
from time import time

HOST = '172.20.10.11' # adresse ip du serveur
PORT = 63678
CODE = 'utf8'
liste=[]
client1=""
client2=(0, 0)


mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    mySocket.bind((HOST, PORT))
except socket.error:
    print("La liaison du socket à l'adresse choisie a échoué.")
    raise

def envoie(clientMsg,destinataire):
    destinataire[1].send(bytes(clientMsg, CODE))

def t1(adresse,destinataire, connexion):
    destinataire[1].send(bytes("connecté", CODE))
    print(f"Client connecté, adresse IP {adresse[0][0]}, port {adresse[0][1]}")

    #adresse[1].send(bytes("Vous êtes connecté au serveur. " + \
                         #"Envoyez vos messages.", CODE))
    serverMsg = ""
    while 1:


        clientMsg = adresse[1].recv(2048).decode(CODE)
        threading.Thread(target=envoie, daemon=True, args=(clientMsg, destinataire, )).start()
        print(adresse, clientMsg)
        if clientMsg.lower() == "stop" or clientMsg == "":
            serverMsg = '__STOP'
            adresse[1].send(bytes(serverMsg, CODE))
            break





    connexion.send(bytes("Au revoir !", CODE))
    print("Connexion interrompue.")
    connexion.close()


while 1:
    print("Serveur prêt, en attente de requêtes ...")
    mySocket.listen(5)

    connexion, adresse = mySocket.accept()


    if client1=="":
        client1=(adresse, connexion)
        print("connecté a client1")
    else:
        client2=(adresse, connexion)
        print("connecté a client2")
        print(client1, client2)
        threading.Thread(target=t1, daemon=False, args=(client1, client2, connexion,)).start()
        threading.Thread(target=t1, daemon=False, args=(client2, client1,connexion, )).start()









