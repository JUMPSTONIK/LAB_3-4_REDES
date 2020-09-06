import threading
import socket
import pickle
import modelos
HEADERSIZE = 10
typeEncode = 'utf-8'

host = '127.0.0.1' #localhost
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
nicknames = []

#mandamos mensaje a todos
def broadcast(message):
    for client in clients:
        client.send(message)

#maneja los mensajes recibidos
def handle(client):
    while True:
        try:
            paquete = recv_obj(client)
            send_obj(clients[nicknames.index(paquete.get_nextNode())],paquete) 
        except:
            index =  clients.index(client)
            clients.remove(client)
            client.close()
            nickname =  nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode(typeEncode))
            nicknames.remove(nickname)
            break

#aceptamos a los clientes
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode(typeEncode))
        nickname = client.recv(1024).decode(typeEncode)
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode(typeEncode))
        client.send('Connected to the server!'.encode(typeEncode))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

#con este podemos enviar objetos a otros clientes
def send_obj(conn,o):
    #print("a")
    obj = pickle.dumps(o)
    #print("b")
    obj = bytes(f"{len(obj):<{HEADERSIZE}}", 'utf-8') + obj
    #print("c")
    conn.send(obj)
    #print("d")

#con esta funcion podemos recibir objetos que nos manden
def recv_obj(conn):
    obj = conn.recv(1024)
    obj = pickle.loads(obj[HEADERSIZE:])
    return obj

print('Server is listening...')
receive()
