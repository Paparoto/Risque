import socket
import threading

clients = []
pret=[]

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

