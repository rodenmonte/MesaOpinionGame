from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.time import StagedActivation
from mesa.datacollection import DataCollector
import numpy as np
import random
import potentials
import math

def clamp(n):
    if n > 1:
        return 1
    elif n < 0:
        return 0
    else:
        return n

class OpinionAgentParameters():
    '''
    For organizational purposes

    Keyword arguments:
    unique_id -- Integers between 0 an N - 1, where N is the total number of agents in a model.
    model -- An instance of OpinionModel.
    neighbors -- A 2d array, size NxAny, use neighbors.py to generate.
    potential -- A potential function, use potentials.py to generate.
    '''
    def __init__(self, unique_id, model, neighbors=None, potential=None, opinions=None, noiseStrength=0.001):
        self.unique_id = unique_id
        self.model = model
        self.neighbors = neighbors
        self.potential = potential
        self.opinions = opinions
        self.noiseStrength = noiseStrength

class OpinionAgent(Agent):
    '''
    An agent has an opinion, and is inlfuenced by other agent\'s 
    opinions based off a potential energy function.

    Keyword arguments:
    params -- An instance of OpinionAgentParameters
    '''
    def __init__(self, params):
        super().__init__(params.unique_id, params.model)
        self.opinions = [op for op in params.opinions]
        self.nextOpinion = [op for op in params.opinions]
        self.neighbors = params.neighbors
        self.potential = params.potential
        self.interacted = False
        self.noiseStrength = params.noiseStrength
    
    def reset(self):
        self.interacted = False
        for i in range(len(self.opinions)):
            self.opinions[i] = self.nextOpinion[i]
    def pairwiseStep(self):
        if self.interacted:
            return
        
        #neighbors_copy is all neighbors not interacted with and not oneself.
        neighbors_copy = [neighb for neighb in self.neighbors if not self.model.schedule.agents[neighb].interacted and self.model.schedule.agents[neighb].unique_id != self.unique_id]
        neighbors_copy_len = len(neighbors_copy)
        '''
        while neighbors_copy: #is not []
            rand_index = np.random.randint(0, neighbors_copy_len) 
            other_agent = self.neighbors[rand_index]
            neighbors_copy.pop(rand_index)
            neighbors_copy_len -= 1
            if self.model.schedule.agents[other_agent].unique_id == self.unique_id:
                continue
            if self.model.schedule.agents[other_agent].interacted:
                continue
            break
        '''
        if not neighbors_copy: #neighbors_copy is of length 0.
            self.interacted = True
            return
        
        rand_index = np.random.randint(0, neighbors_copy_len) 
        other_agent = self.neighbors[rand_index]
        
        for i in range(len(self.opinions)):
            difference = self.opinions[i] - self.model.schedule.agents[other_agent].opinions[i]
            self.nextOpinion[i] += (self.model.ALPHA / 2) * self.potential(self, self.model.schedule.agents[other_agent], i) * (difference / (abs(difference) + .0001)) #Replace small number with EPSILON constant later
            #change the other agent's opinion too!
            self.model.schedule.agents[other_agent].nextOpinion[i] -= (self.model.ALPHA / 2) * self.model.schedule.agents[other_agent].potential(self, self.model.schedule.agents[other_agent], i) * (difference / (abs(difference) + .0001))

            self.model.schedule.agents[other_agent].nextOpinion[i] = clamp(self.model.schedule.agents[other_agent].nextOpinion[i])
            self.nextOpinion[i] = clamp(self.nextOpinion[i])
            self.model.schedule.agents[other_agent].interacted = True
            self.interacted = True

    def simultaneousStep(self):
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
                if difference != 0: #Avoid division by 0.
                    #The negative is in the potential function.
                    self.nextOpinion[i] += (self.model.ALPHA / 2) * self.potential(self, self.model.schedule.agents[other], i) * (difference / abs(difference))
                self.nextOpinion[i] = clamp(self.nextOpinion[i])

    def simultaneousAdvance(self):
        for i in range(len(self.opinions)):
            self.opinions[i] = self.nextOpinion[i]

    def coupling(self):
        #Coupling
        changes = [0 for i in self.opinions]
        for i in range(len(self.opinions)):
            for j in range(len(self.opinions)):
                #o[i]^t+1 += 1/c_ij * change_in(o[j] ^t).
                change_in_opinion = self.nextOpinion[j] - self.opinions[j]
                changes[i] += self.model.coupling[i][j] * change_in_opinion
        #Differences will change if opinions aren't updated afterwards...
        for i in range(len(self.opinions)):
            self.nextOpinion[i] = changes[i] + self.opinions[i]
            self.nextOpinion[i] = clamp(self.nextOpinion[i])

    def noise(self):
        for i in range(len(self.opinions)):
            noise_size = 0
            for j in range(len(self.neighbors)):
                noise_size += pow(math.e, -1 * (self.opinions[i] - self.model.schedule.agents[j].opinions[i]))
            noise_size = self.noiseStrength * noise_size
            self.nextOpinion[i] += np.random.normal(0, noise_size)
            self.nextOpinion[i] = clamp(self.nextOpinion[i])

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
    coupling -- AxA matrix, where A = |opinions|. Describes how
    opinions affect each other.
    '''
    def __init__(self, N, neighborhoods, initial_opinions, potentials, coupling, schedule="simultaneous"):
        self.ALPHA = .001
        self.num_agents = N
        self.neighborhoods = neighborhoods
        self.initial_opinions = initial_opinions
        self.potentials = potentials
        self.coupling = coupling
        
        #Set schedule
        if schedule == 'simultaneous':
            self.schedule = StagedActivation(self, stage_list=["simultaneousStep", "simultaneousAdvance"], shuffle=False)
        elif schedule == 'pairwise':
            self.schedule = StagedActivation(self, stage_list=["reset", "pairwiseStep"], shuffle=True)
            #stage_list is where you add "coupling" and "noise". 

        #Create agents
        for i in range(self.num_agents):
            a_params = OpinionAgentParameters(i, self, self.neighborhoods[i], self.potentials[i], initial_opinions[i])
            if schedule == 'simultaneous':
                a = OpinionAgent(a_params)
            elif schedule == 'pairwise':
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
