import socket
import threading

clients = []
pret=[]

class Pays:
    def __init__(self, nom, liste_adjacents, position:tuple, troupes:int, rendement:int, couleur="blanc"):
        self.nom = nom
        self.liste_adjacents = liste_adjacents
        self.position = position
        self.troupes = troupes
        self.rendement = rendement
        self.couleur=couleur

    def __str__(self):
        return self.nom

    def deplacement(self, autre_pays):
        if autre_pays not in self.liste_adjacents :
            return "impossible"
        elif autre_pays.couleur == self.couleur:
            autre_pays.troupes+= self.troupes
            self.troupes=0
        elif self.troupes<autre_pays.troupes:
            autre_pays.troupes -= self.troupes
            self.troupes = 0

        elif self.troupes>autre_pays.troupes:
            autre_pays.couleur = self.couleur
            autre_pays.troupes = self.troupes - autre_pays.troupes
            self.troupes=0

        elif self.troupes == autre_pays.troupes:
            self.troupes = 0
            autre_pays.troupes = 0

    def augmenter_armée(self):
        if self.couleur == "blanc":
            return
        else:
            self.troupes += self.rendement


def broadcast(message, conn):
    for client in clients:
        if client != conn:
            client.send(message)

def handle_client(conn):

    while True:
        try:
            message = conn.recv(1024)
            msg=message.decode("utf-8")
            if msg=="pret":
                if conn == clients[1]:
                    start = "start"
                    start = start.encode("utf-8")
                    for conn in clients:
                        conn.send(start)

            message=msg.encode("utf-8")
            print(msg)

            if message:
                broadcast(message, conn)
            else:
                conn.close()
                clients.remove(conn)
                break
        except:
            conn.close()
            clients.remove(conn)
            break

def main():
    host = socket.gethostname()
    print(host)
    port = 50000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print("Server started on port", port)

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        acceuil = "Vous etes client" + str(clients.index(conn)+1)
        acceuil=acceuil.encode("utf-8")
        conn.send(acceuil)


        print(f"Connection from {addr}, client{clients.index(conn)+1}")
        thread = threading.Thread(target=handle_client, args=(conn,))
        thread.start()

if __name__ == "__main__":
    main()



