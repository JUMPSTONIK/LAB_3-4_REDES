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

graph = {'a':{'b':10,'c':3},'b':{'c':1,'d':2},'c':{'b':4,'d':8,'e':2},'d':{'e':7},'e':{'d':9}}
 
def dijkstra(graph,start,goal):
    shortest_distance = {}
    predecessor = {}
    unknowNodes = graph
    infinity = 9999999
    list_of_jumps = {}
    distance = 0
    path = []
    for node in unknowNodes:
        shortest_distance[node] = infinity
    shortest_distance[start] = 0
 
    while unknowNodes:
        minNode = None
        for node in unknowNodes:
            if minNode is None:
                minNode = node
            elif shortest_distance[node] < shortest_distance[minNode]:
                minNode = node
        jumps = []
        for childNode, weight in graph[minNode].items():
            if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                shortest_distance[childNode] = weight + shortest_distance[minNode]
                predecessor[childNode] = minNode
        #print(jumps)
        unknowNodes.pop(minNode)
    
    currentNode = goal
    while currentNode != start:
        try:
            path.insert(0,currentNode)
            currentNode = predecessor[currentNode]
        except KeyError:
            print('Path not reachable')
            break
    path.insert(0,start)
    if shortest_distance[goal] != infinity:
        print('And the path is ' + str(path))
        return path

 
#dijkstra(graph, 'a', 'd')

write_thread = threading.Thread(target=write)
write_thread.start()