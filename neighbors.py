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
