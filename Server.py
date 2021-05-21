import socket
import threading

host = '127.0.0.1'
port = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


def recieve():
    while True:
        
        client, address = server.accept()  #Accept Connection
        print(f"Connected With {str(address)}!")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)


        print(f"Nickname of the Client {nickname}")
        broadcast(f"{nickname} Connected To the Server! \n".encode('utf-8'))
        client.send("Connected to the Srever".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(clients, ))
        thread.start()


print("Server is Running .. ")
recieve()   
