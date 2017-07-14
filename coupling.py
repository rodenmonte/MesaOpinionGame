'''
Each function in the module generates square matrices.
Thse matrices correspond to opinion coupling as described in
section 3.6 of the paper.
'''
import numpy as np

no_coupling(n):
    '''
    Returns the identity matrix, size n.

    Keyword argument:
    n -- The number of opinions in a system, and the size of the coupling matrix.
    '''
    coupling = []
    for i in range(n):
        inner = []
        for j in range(n):
            if i == j:
                inner.append(1)
            else:
                inner.append(0)
        coupling.append(inner)
    return coupling

random_coupling(n, min=0, max=1):
    '''
    Returns an nxn matrix with random values, all between 1 and 0. 

    Keyword argument:
    n -- The number of opinions in a system, and the size of the coupling matrix.
    '''
    coupling = []
    for i in range(n):
        inner = []
        for j in range(n):
            inner.append(np.random.rand())
        coupling.append(inner)
    return coupling
