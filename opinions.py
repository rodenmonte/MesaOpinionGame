from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
import numpy as np
import potentials

class OpinionParameters():
    '''
    For organizational purposes

    Keyword arguments:
    unique_id -- Integers between 0 an N - 1, where N is the total number of agents in a model.
    model -- An instance of OpinionModel.
    neighbors -- A 2d array, size NxAny, use neighbors.py to generate.
    potential -- A potential function, use potentials.py to generate.
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
    opinions based off a potential energy function.

    Keyword arguments:
    params -- An instance of OpinionParameters.
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
        for other in self.neighbors: #Other is an index.
            for i in range(len(self.opinions)):
                difference = self.opinions[i] - self.model.schedule.agents[other].opinions[i]
                if difference == 0:
                    pass
                else:
                    #The negative is in the potential function.
                    self.nextOpinion[i] += (self.model.ALPHA / 2) * self.potential(self, self.model.schedule.agents[other], i) * (difference / abs(difference))
                # Clamp function
                if self.nextOpinion[i] > 1:
                    self.nextOpinion[i] = 1
                elif self.nextOpinion[i] < 0:
                    self.nextOpinion[i] = 0
    def advance(self):
        for i in range(len(self.opinions)):
            self.opinions[i] = self.nextOpinion[i]

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
        '''
        Advance the model one step
        '''
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
