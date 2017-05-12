import numpy as np
def totally_connected(N, self_connected=False):
    '''
    Returns an nxn matrix.
    
    Keyword arguments:
    N -- the number of nodes in the network
    self_connected -- If a node is self connected, it will
    be in its own neighbors matrix.
    '''
    neighborhood = []
    for i in range(N):
        neighbors = []
        for j in range(N):
            #We don't necesarrily want self-reference.
            if(i != j):
                neighbors.append(j)
            #BUT if we do want self-reference:
            elif(self_connected):
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
    #The name total_connections is a lie
    #In this implementation, the actual number of total
    #connections is less than or equal to total_connections
    #But current_connections can be used to make sure
    #total_connections is met, in the future.
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

#TODO cluster_connected
#Takes 3 parameters, N, degree, and n_clusters
#degree is the degree of connection BETWEEN CLUSTERS.
#n_clusters is the number of clusters.
#Perhaps it is as easy as a combination of the previous two methods?
