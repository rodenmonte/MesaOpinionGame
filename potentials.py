'''
The functions below are the negatives of the derivatives they represent in the paper.
Note that these functions return functions, not values. TODO tell the user where these functions can be found in the paper. Perhaps implement other potential functions?
'''
from math import e
from math import pow
from math import sqrt
from math import pi
def tent(tau_l=.5, tau_u=None): 
    #If only one tent peak is wanted
    if(tau_u == None):
        tau_u = tau_l
    #This case arises if the funciton is not properly initialized
    #The fix just switches the points of the plateau
    elif(tau_u > tau_l):
        temp = tau_u
        tau_u = tau_l
        tau_l = temp

    def impl(diff):
        if(diff < tau_l): #Left half of the potential function.
            return -1 * (1 / tau_l) #Rise over run, times -1, because its a potential function.
        elif(diff > tau_u):
            return 1 * (1 / (1 - tau_u)) #the x distance between the end of y=1 and y=0 is 1 - tau_u.
        else:
            return 0
    return impl

def bcm(tau):
    '''
    As in 3.5.4 of the paper.
    '''
    def impl(diff):
        if(diff <= tau):
            return 2 * diff
        else:
            return 0
    return impl

def gaussian(mean=.5, stddev=.5):
    #Recall the gaussian is: (1 / (u * sqrt( 2 * pi)) * e ^ (- x^2 / (2 * u^2)), and we care about its derivative in terms of x (the mean), which gives its graphical slope. 
    def impl(diff):
        return 1 * (diff - mean) / (pow(stddev, 3) * sqrt(2 * pi)) * pow(e, -1 * pow(diff - mean, 2) / (2 * pow(stddev, 2)))
    return impl

def simple():
    def impl(diff=0): #Default parameter here, because it has no effect. If someone decides not to use a parameter in this case, it won't break their code. A function is returned only to maintain form with the other potential functions
        return -1
    return impl

