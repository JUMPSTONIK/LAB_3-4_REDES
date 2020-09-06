import socket
import threading
import pickle
graph = {'a':{'b':10,'c':3},'b':{'c':1,'d':2},'c':{'b':4,'d':8,'e':2},'d':{'e':7},'e':{'d':9}}
HEADERSIZE = 10
typeEncode = 'utf-8'

nickname = input("choose a nickname: ")

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

class paquete(object):

    def __init__(self, type_alg, mensaje, ori, go):
        self.algorithm = type_alg
        self.msg = mensaje
        self.origin = ori
        self.goal = go
        self.path = None
        self.maxJumps = None
        self.pastNode = None
        self.jumps = None
        self.distance = None
        self.nextNode = None
        self.sendingNode = None

    def get_algorithm():
        return self.algorithm

    def get_msg():
        return self.msg

    def get_orgigin():
        return self.origin

    def get_goal():
        return self.goal

    def get_path():
        return self.path

    def set_path(the_path):
        self.path = the_path

    def get_maxJumps():
        return self.maxJumps

    def set_maxJumps(total_jumps):
        self.maxJumps = total_jumps

    def get_pastNode():
        return self.pastNode

    def set_pastNode(pNode):
        self.pastNode = pNode

    def get_jumps():
        return self.jumps

    def set_jumps(nJumps):
        self.jumps = nJumps

    def get_distance():
        return self.distance

    def set_distance(dist):
        self.distance = dist

    def get_nextNode():
        return self.nextNode

    def set_nextNode(nNode):
        self.nextNode = nNode

    def get_sendingNode():
        return self.sendingNode

    def set_sendingNode(sNode):
        self.sendingNode = sNode


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