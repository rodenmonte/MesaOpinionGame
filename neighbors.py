import numpy as np
import networkx as nx
from math import isclose
def weight_to_neighbors(weights):
    '''
    Returns a neighborhood matrix from a weight matrix.
    Weights close to 0 are ommitted.
    A 2d array of weights is returned.

    Keyword Arguments:
    weights -- A 2D array of weights. weights must be square.
    '''
    neighborhood = []
    for i in range(len(weights)):
        neighbors = []
        for j in range(len(weights[i])):
            if not isclose(weights[i][j], 0.0):
                neighbors.append(j)
        neighborhood.append(neighbors)
    return neighborhood
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

def graph_to_matrix(g):
    '''
    Converts a networkx graph into a list of lists. Doesn't preserve weight.

    Keyword arguments:
    g -- A networkx graph.
    '''
    matrix = []
    new_graph = nx.to_dict_of_lists(g)
    for i in range(len(new_graph)):
        matrix.append(new_graph[i])
    return matrix

def matrix_to_graph(m):
    '''
    Takes a neighbordhood matrix m and converts it to a networkx graph.

    Keyword arguments:
    m -- An nxn neighborhood matrix.
    '''
    graph_dict = {}
    for i in range(len(m)):
        graph_dict[i] = m[i]
    return nx.from_dict_of_lists(graph_dict)
