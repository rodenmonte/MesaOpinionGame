import numpy as np
def totally_connected(N):
    '''
    Returns an nxn matrix.
    
    Keyword arguments:
    N -- the number of nodes in the network
    '''
    neighborhood = []
    for i in range(N):
        neighbors = []
        for j in range(N):
            if(i != j):
                neighbors.append(j)
        neighborhood.append(neighbors)
    return neighborhood

def degree_connected(N, degree):
    '''
    Returns an nxn matrix as nested lists.
    Pseudorandom connections,
    every node will have at least the average number of connections.

    Keyword arguments:
    N -- The number of nodes in the network.
    degree -- A float ranging from 0 to 1.
    Degree determines how connected the graph will be.
    1 is a totally connected graph, 0 is totally disconnected.
    '''
    neighborhood = []
    max_connections = N * (N - 1)
    total_connections = int(degree * max_connections)
    average_connections = int(total_connections / N)
    current_connections = 0
    shuffler = [i for i in range(N)]
    for i in range(N):
        neighbors = []
        np.random.shuffle(shuffler)
        for j in range(average_connections):
            if i == shuffler[j]: #Can't connect to itself!
                #Append the last element of the list
                #As it will NEVER be run into otherwise.
                neighbors.append(shuffler[-1])
            else:
                neighbors.append(shuffler[j])
        neighborhood.append(neighbors)
        current_connections += average_connections
    return neighborhood
