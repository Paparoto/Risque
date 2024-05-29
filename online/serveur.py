import socket
import threading

clients = []

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
        print(f"Connection from {addr}")
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn,))
        thread.start()

if __name__ == "__main__":
    main()
