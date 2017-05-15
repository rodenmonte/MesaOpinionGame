'''
The functions below are the negatives of the derivatives they represent in the paper.
Note that these functions return functions, not values. TODO tell the user where these functions can be found in the paper. Perhaps implement other potential functions?
'''
from math import e
from math import pow
from math import sqrt
from math import pi
def tent(tau_l=.5, tau_u=.5): 
    '''
    Return a tent function, which gives negative gradient function values
    determined by difference in opinions. See Section 3.4 of the paper.

    Keyword arguments:
    tau_l -- The first peak or lower peak. Defaults to .5.
    If only tau_l is given, the tent function has only one peak.
    0 <= tau_l <= 1
    tau_u -- The end of the plateau. 
    Note that if tau_u > tau_l on assignment, the values are switched.
    0 <= tau_u <= 1
    '''
    if(tau_u > 1):
        tau_u = 1
    if(tau_l < 0):
        tau_l = 0

    #If only one tent peak is wanted
    #Note that we must use 'is' which is an identity comparison, not ==.
    if(tau_u is None):
        tau_u = tau_l
    #This case arises if the function is not properly initialized
    #The fix just switches the points of the plateau
    elif(tau_l > tau_u):
        temp = tau_u
        tau_u = tau_l
        tau_l = temp

    def impl(agent1, agent2, i):
        diff = abs(agent1.opinions[i] - agent2.opinions[i])
        if(diff < tau_l): #Left half of the potential function.
            #Note that a 0 divide error will never be risen.
            #diff > 0, and tau_l < diff.
            return -1 * (1 / tau_l)
        elif(diff > tau_u):
            #A 0 divide error will never be risen because diff < 1
            #So if tau_u = 1, this clause will never be run.
            return 1 * (1 / (1 - tau_u))
        else:
            return 0
    return impl

def bcm(tau):
    '''
    Bounded Confidence Model
    Returns a function returning 2*diff if x <= tau, 0 otherwise.

    Keyword argument:
    tau -- Marks the point of flatline as seen in 3.4 Fig 2. part d.
    0 <= tau <= 1.
    '''
    def impl(agent1, agent2, i):
        diff = abs(agent1.opinions[i] - agent2.opinions[i])
        if(diff <= tau):
            return 2 * diff
        else:
            return 0
    return impl

def gaussian(mean=.5, stddev=.5):
    '''
    Returns a function returning the derivative of the gaussian at
    the difference of two agents' opinion i. The default values
    approximately match the curve given in 3.5 of the paper.

    Keyword arguments:
    mean -- the mean used to construct a gaussian, defaulted to .5, as
    that makes sense in the context of the model
    stddev -- the standard deviation used to construct the model Based on
    tested values, .5 makes sense as a default value, as it yields a slopes
    of ~-1 and ~1 at differences of 0 and 1 respectively. Obviously, a
    difference of value = mean yields derivative 0.
    #Recall the gaussian is: (1 / (u * sqrt( 2 * pi)) * e ^ (- x^2 / (2 * u^2)), and we care about its derivative in terms of x (the mean), which gives its graphical slope. 
    '''
    def impl(agent1, agent2, i):
        diff = abs(agent1.opinions[i] - agent2.opinions[i])
        return 1 * (diff - mean) / (pow(stddev, 3) * sqrt(2 * pi)) * pow(e, -1 * pow(diff - mean, 2) / (2 * pow(stddev, 2)))
    return impl

def simple():
    '''
    Returns a function that always returns -1.
    In a model without a noise function, this should always lead
    to consensus.
    '''

    def impl(agent1, agent2, i):
        '''
        Note the parameters have no effect, but are there to maintain
        form with the other potential functions.
        '''
        return -1
    return impl

def flat():
    '''
    Returns a function always returning 0.
    May be useful for tests.
    '''
    def impl(a1, a2, i):
        return 0;
    return impl



def french():
    '''
    As in the paper. If other parameters are adjusted accordingly,
    this will yield the update rule:
    o_i^(t+1) = 1/(k+1) * sum of innode opinions at time t.
    This is explained on page 16/42 of the paper, or section 3.5.4.
    '''
    def impl(agent1, agent2, i):
        k = len(agent1.neighbors)
        if(agent1.unique_id == agent2.unique_id):
            return k * agent1.opinions[i] / (k + 1)
        else:
            return -agent2.opinions[i] / (k + 1)
    return impl

def degroot(P):
    '''
    Returns a potential function. See section 3.5.4.

    Keyword arguments:
    P -- NxN matrix of "weights". N = then number of agents in a matrix.
    '''
    def impl(agent1, agent2, i):
        a1uid = agent1.unique_id
        a2uid = agent2.unique_id
        if(a1uid == a2uid):
            return (P[a1uid][a1uid] - 1) * agent1.opinions[i]
        else:
            return P[a1uid][a2uid] * agent2.opinions[i]
    return impl

def simple2():
    '''
    Returns a function returning the negative of the difference
    between two opinions
    '''
    def impl(agent1, agent2, i):
        diff = abs(agent1.opinions[i] - agent2.opinions[i])
        return -1 * diff
    return impl
