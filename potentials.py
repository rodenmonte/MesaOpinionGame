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
    if(tau_u == None):
        tau_u = tau_l
    #This case arises if the function is not properly initialized
    #The fix just switches the points of the plateau
    elif(tau_u > tau_l):
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
    #Recall the gaussian is: (1 / (u * sqrt( 2 * pi)) * e ^ (- x^2 / (2 * u^2)), and we care about its derivative in terms of x (the mean), which gives its graphical slope. 
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

##def french():
##    '''
#    '''
#    def impl(agent1, agent2, i):
#        #The number of indegrees IS agent.neighbors.
#        #This is passed in as k.
#        if agent1_opinion == agent2_opinion
#
#
