import socket
import threading

clients = []

"""def get_client_number(conn):
    return clients.index(conn)+1"""

def broadcast(message, conn):
    for client in clients:
        if client != conn:
            client.send(message)

def handle_client(conn):
    while True:
        try:

            message = conn.recv(1024)

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
    port = 50000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print("Server started on port", port)

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        print(f"Connection from {addr}, client{clients.index(conn)+1}")
        thread = threading.Thread(target=handle_client, args=(conn,))
        thread.start()

if __name__ == "__main__":
    main()