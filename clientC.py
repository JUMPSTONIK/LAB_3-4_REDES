import socket
import threading
import pickle
from modelos import paquete
import time
import traceback
import copy

HEADERSIZE = 10
typeEncode = 'latin-1'
neighborNames=["a","d"]
neighborCosts=[1,4]
ip=input("Ingrese la dirección para conectarse: ")
port=int(input("Ingrese el numero de puerto: "))
nickname = "c"

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((ip, port))

def send_message(mensaje,neighborNum):
    global neighborNames
    global neighborCosts
    global nickname
    nodes=mensaje.get_pastNode()
    nodes.append(nickname)
    mensaje.set_nextNode(neighborNames[neighborNum])
    mensaje.set_sendingNode(nickname)
    mensaje.set_distance(mensaje.get_distance()+neighborCosts[neighborNum])
    mensaje.set_jumps(mensaje.get_jumps()+1)
    mensaje.set_pastNode(nodes)
    send_obj(mensaje)

def send_flood(mensaje):
    global neighborNames
    global neighborCosts
    for i in range(len(neighborNames)):
        if (neighborNames[i] != mensaje.get_sendingNode()):
            a=copy.deepcopy(mensaje)
            send_message(a,i)

def send_directed(mensaje):
    global neighborCosts
    global neighborNames
    global nickname
    pathASeguir = mensaje.get_path()
    pos=pathASeguir.index(nickname)+1
    send_message(mensaje,neighborNames.index(pathASeguir[pos]))

def print_message_recieved(mensaje):
    print("Nodo origen: "+mensaje.get_origin())
    print("Nodo destino: "+mensaje.get_goal())
    print("Mensaje: "+mensaje.get_msg())
    print("Nodos pasados: ")
    print(mensaje.get_pastNode())
    print("Saltos: "+str(mensaje.get_jumps()))
    print("Distancia recorrida: "+str(mensaje.get_distance()))

def  recieve():
    global nickname
    while True:
        try:
            message = client.recv(1024)
            a=message.decode(typeEncode).strip()
            if a == 'NICK':
                client.send(nickname.encode(typeEncode))
            elif a!=None:
                mensajeReciv=pickle.loads(message[HEADERSIZE:])
                if (mensajeReciv.get_goal()!=nickname):
                    a=copy.deepcopy(mensajeReciv)
                    nodes=a.get_pastNode()
                    nodes.append(nickname)
                    a.set_pastNode(nodes)
                    print_message_recieved(a)
                    if(mensajeReciv.get_algorithm()==1):
                        if (mensajeReciv.get_jumps()<mensajeReciv.get_maxJumps()):
                            send_flood(mensajeReciv)
                    else:
                        send_directed(mensajeReciv)
                else:
                    nodes=mensajeReciv.get_pastNode()
                    nodes.append(nickname)
                    mensajeReciv.set_pastNode(nodes)
                    print_message_recieved(mensajeReciv)
        except:
            print("an error ocurred!")
            traceback.print_exc()
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