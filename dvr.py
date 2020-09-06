def dvr(graph, source):
    distance, predecessor = dict(), dict()
    for node in graph:
        distance[node], predecessor[node] = float('inf'), None
    distance[source] = 0

    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbour in graph[node]:
                if distance[neighbour] > distance[node] + graph[node][neighbour]:
                    distance[neighbour], predecessor[neighbour] = distance[node] + graph[node][neighbour], node

    return distance, predecessor

graph = {
    'a': {'b': 5, 'i': 3, 'c': 1},
    'b': {'a': 5, 'f': 8},
    'c': {'a': 1, 'd': 4},
    'd': {'i': 7, 'c': 4, 'f': 3, 'e': 9},
    'e': {'d': 9, 'g': 5},
    'f': {'b': 8, 'd': 3, 'g': 4, 'h': 3},
    'g': {'f': 4, 'e': 5},
    'h': {'f': 3},
    'i': {'a': 3, 'd': 7},
}

distance, predecessor = dvr(graph, source='h')

print(distance)
print(predecessor)
