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
        print('nodo fuente: ' + start)
        print('nodo destino: ' + goal)
        jumps(graph,path,start)
        print('saltos recorridos: ' + str(list_of_jumps))
        print('distancia recorrida: ' + str(shortest_distance[goal]))
        print('And the path is ' + str(path))

def jumps(grafo, trayectoria, inicio):
        for x in range(0,len(trayectoria)-1):
            print(graph[trayectoria[x]][trayectoria[x]])
 
dijkstra(graph, 'a', 'd')
