from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
import numpy as np
import potentials

class OpinionParameters():
    '''
    For organizational purposes
    #Neighbors is an array. If no argument is given for neighbors, then it is assumed that the graph is totally connected. TODO: Implement ways to easily make pairwise graphs, varying degrees of connectedness in graphs, etc. These ways can be based solely on the size of the array.
    #Potentials can be an array. len(potentials) == len(neighbors). Otherwise, potenials should be one function. If it is left out, a tent function tau = .5 is defaulted to.
    '''
    def __init__(self, unique_id, model, neighbors=None, potential=None, opinions=None):
        self.unique_id = unique_id
        self.model = model
        self.neighbors = neighbors
        self.potential = potential
        self.opinions = opinions

class OpinionAgent(Agent):
    '''
    An agent has an opinion, and is inlfuenced by other agent\'s 
    opinions based off a potential energy function. For now, initial 
    opinion of an agent is random
    '''
    #Params is an instance of OpinionParameters
    def __init__(self, params):
        super().__init__(params.unique_id, params.model)
        self.opinions = [op for op in params.opinions]
        self.nextOpinion = [op for op in params.opinions]
        self.neighbors = params.neighbors
        self.potential = params.potential
    def step(self):
        '''
        Calculates next opinion based off of all other agent's
        opinions. Models a totally connected graph.
        o_i^(t+1) = o_i^t + sum(j = 1 to k, (- alpha / 2) * potential'(|diff|) * diff/ |diff| is the formula for the  next opinion from the paper.
        1 to k represents all neighbors.
        '''
        # This calculates the next opinion based off the formula
        for other in self.neighbors: #Other is just a number.
            for i in range(len(self.opinions)):
                difference = self.opinions[i] - self.model.schedule.agents[other].opinions[i]
                if difference == 0:
                    pass
                else:
                    #The negative is in the potential function now.
                    self.nextOpinion[i] += (self.model.ALPHA / 2) * self.potential(self, self.model.schedule.agents[other], i) * (difference / abs(difference))
                # Clamp function
                if self.nextOpinion[i] > 1:
                    self.nextOpinion[i] = 1
                elif self.nextOpinion[i] < 0:
                    self.nextOpinion[i] = 0
    def advance(self):
        for i in range(len(self.opinions)):
            self.opinions[i] = self.nextOpinion[i]
            #We don't need to change nextOpinion[i], it is inconsequential. We could make it None so that exceptions would be raised if it was attempted to be used or hadn't been set. 

class OpinionModel(Model):
    '''
    A model with some number of agents

    Keyword arguments:
    N -- Number of agents
    neighborhoods -- An NxX matrix.
    neighborhoods[a] is agent a's list of neighbors.
    The neighborhoods is not actually a matrix.
    Each inner list may be of different length.
    intial_opinions -- This is a list size N of opinions.
    Each inner list must have the same length, the opinions
    are then labeled Opinion0, Opinion1, ..., OpinionZ.
    potentials -- Potentials is a 1-D list of functions
    Each function describes how agents are influenced by innodes.
    '''
    def __init__(self, N, neighborhoods, initial_opinions, potentials):
        self.ALPHA = .001
        self.num_agents = N
        self.neighborhoods = neighborhoods
        self.initial_opinions = initial_opinions
        self.potentials = potentials
        self.schedule = SimultaneousActivation(self)
        #Create agents
        for i in range(self.num_agents):
            #TODO Remove below 2 comments, after new neighborhood method works.
            #neighbors = [random.randint(0, N-1) for i in range((N + 3) // 4)]
            #neighbors = [i for i in range(N)]
            a_params = OpinionParameters(i, self, self.neighborhoods[i], self.potentials[i], initial_opinions[i])
            a = OpinionAgent(a_params)
            self.schedule.add(a)

        ag_reps = dict()
        for i in range(len(self.schedule.agents[0].opinions)):
            ag_reps["Opinion" + str(i)] = self.makeLam(i)

        self.datacollector = DataCollector(
                agent_reporters = ag_reps
        )
        
    def step(self):
        '''Advance the model one step'''
        self.datacollector.collect(self)
        self.schedule.step()

    def run(self, steps):
        for i in range(steps):
            self.step()

    def makeLam(self, i):
        '''
        Don't use outside of the context of the OpinionModel's init method.
        This function is needed in order for the DataCollector to work properly,
        intializing the lambdas inside __init__ inside a for loop causes the last
        value of the iterator to be used for all of the functions, causing
        unwanted behavior. So that's why this function exists.
        '''
        return lambda a: a.opinions[i]
