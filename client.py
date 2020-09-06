import socket
import threading
import pickle
HEADERSIZE = 10
typeEncode = 'utf-8'

nickname = input("choose a nickname: ")

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

def  recieve():
    while True:
        try:
            message = client.recv(1024).decode(typeEncode)
            if message == 'NICK':
                client.send(nickname.encode(typeEncode))
            else:
                print(message)
        except:
            print("an error ocurred!")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode(typeEncode))

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

#con este podemos enviar objetos a otros clientes
def send_obj(o):
    obj = pickle.dumps(o)
    obj = bytes(f"{len(obj):<{HEADERSIZE}}", 'utf-8') + obj
    client.send(obj)

#con esta funcion podemos recibir objetos que nos manden
def recv_obj():
    obj = client.recv(1024)
    data = pickle.loads(obj[HEADERSIZE:])
    return data

write_thread = threading.Thread(target=write)
write_thread.start()