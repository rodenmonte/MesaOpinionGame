import scipy.io as sio
def read(filename):
    '''
    Determines the type of file we're dealing with, calls
    the appropriate function to turn the file into a weight matrix.

    Keyword Arguments:
    filename -- A file name or path to a .mtx, .mat, or .rb file.
    '''
    if filename.endswith('.mtx'):
        return read_mtx(filename)

    elif filename.endswith('.mat'):
        return read_mat(filename)

    elif filename.endswith('.rb'):
        raise Exception('.rb not supported yet.')

    else:
        raise Exception('Filetype not recognized.')

def read_mtx(filename):
    '''
    Returns an array representing an adjacency matrix.

    Keyword Arguments:
    filename -- A .mtx (Matrix Market Format) file with a square matrix representing an
    adjacency matrix.
    '''
    f = sio.mmread(filename)
    a = f.toarray()
    return a

def read_mat(filename):
    '''
    Questionable...
    '''
    f = sio.loadmat(filename)
    a = f['Problem'][0][0][1].toarray()
    return a
