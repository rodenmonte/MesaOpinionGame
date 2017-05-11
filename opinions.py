# Naive implementation of the opinion game. For now, agents are totally connected.
from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
import numpy as np
import random
import potentials

ALPHA = .001 #TEMPORARY, in the future ALPHA should be able to be passed by the user & varied. Recall alpha measures learning rate. Maybe make constants.py to hold just ALPHA?

#GOAL TODO put all the parameters for the model in here, which will be used in OpinionModel to create OpinionAgents easily.
class OpinionParameters():
    '''
    For organizational purposes
    '''
    #Neighbors is an array. If no argument is given for neighbors, then it is assumed that the graph is totally connected. TODO: Implement ways to easily make pairwise graphs, varying degrees of connectedness in graphs, etc. These ways can be based solely on the size of the array. 
    #Potentials can be an array. len(potentials) == len(neighbors). Otherwise, potenials should be one function. If it is left out, a tent function tau = .5 is defaulted to. 
    def __init__(self, unique_id, model, neighbors=None, potential=None, opinions=None):
        self.unique_id = unique_id
        self.model = model
        self.neighbors = neighbors
        self.potential = potential
        self.opinions = opinions


class OpinionAgent(Agent):
    '''
    An agent has an opinion, and is inlfuenced by other agent's opinions based off a potential energy function. For now, initial opinion of an agent is random
    '''
    #Params is an instance of OpinionParameters
    def __init__(self, params):
        super().__init__(params.unique_id, params.model) # sets self.model
        self.opinions = [op for op in params.opinions]
        self.nextOpinion = [op for op in params.opinions]
        self.neighbors = params.neighbors # neighbors are the people an agent is influenced by. As a viewer, I may consider a news channel a "neighbor" of sorts, but they would probably not think of me at all.
        self.potential = params.potential
         
    def step(self):
        '''
        Calculates next opinion based off of all other agent's opinions. Models a totally connected graph.
        o_i^(t+1) = o_i^t + sum(j = 1 to k, (- alpha / 2) * potential'(|diff|) * diff/ |diff| is the formula for the  next opinion from the paper. 1 to k represents all neighbors. 
        '''
        # This calculates the next opinion based off the formula
        for other in self.neighbors: #Other is just a number.
            for i in range(len(self.opinions)):
                difference = self.opinions[i] - self.model.schedule.agents[other].opinions[i]
                if difference == 0: #Don't calculate for the same node. Unsure what to do if there are other nodes of the same opinion, probably doesn't matter at this point
                    pass;
                else:
                    #The negative is in the potential function now.
                    self.nextOpinion[i] += (ALPHA / 2) * self.potential(abs(difference)) * (difference / abs(difference))

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
    '''A model with some number of agents
    LIMITATION: Every agent has the same number of opinions, although an agent can be such that all other agents take no stake in its opinion, and its potential function is such that its opinion does not change.... Not sure how to work around this, given how the data collector must be initialized for multiple opinions.
    '''
    def __init__(self, N):
        self.num_agents = N
        self.schedule = SimultaneousActivation(self)
        #Create agents
        for i in range(self.num_agents):
            #neighbors = [random.randint(0, N-1) for i in range((N + 3) // 4)] #So that nodes don't have 0 neighbors...
            neighbors = [i for i in range(N)]
            a_params = OpinionParameters(i, self, neighbors, potentials.tent(.5), [np.random.rand(), .4])
            a = OpinionAgent(a_params)
            self.schedule.add(a)

        ag_reps = dict();
        for i in range(len(self.schedule.agents[0].opinions)):
            ag_reps["Opinion" + str(i)] = self.makeLam(i);

        self.datacollector = DataCollector(
                agent_reporters = ag_reps
        )
        
    def step(self):
        '''Advance the model one step'''
        self.datacollector.collect(self)
        self.schedule.step()
    def makeLam(self, i):
        return lambda a: a.opinions[i];
