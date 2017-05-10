# Naive implementation of the opinion game. For now, agents are totally connected.
from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
import numpy as np
import random
import potentials

ALPHA = .001 #TEMPORARY, in the future ALPHA should be able to be passed by the user & varied. Recall alpha measures learning rate. Maybe make constants.py to hold just ALPHA?

class OpinionAgent(Agent):
    '''
    An agent has an opinion, and is inlfuenced by other agent's opinions based off a potential energy function. For now, initial opinion of an agent is random
    '''
    def __init__(self, unique_id, model, neighbors, potential):
        super().__init__(unique_id, model) # sets self.model
        self.opinion = np.random.rand() #From 0 to 1
        self.nextOpinion = None
        self.neighbors = neighbors # neighbors are the people an agent is influenced by. As a viewer, I may consider a news channel a "neighbor" of sorts, but they would probably not think of me at all.
        self.potential = potential
         
    def step(self):
        '''
        Calculates next opinion based off of all other agent's opinions. Models a totally connected graph.
        o_i^(t+1) = o_i^t + sum(j = 1 to k, (- alpha / 2) * potential'(|diff|) * diff/ |diff| is the formula for the  next opinion from the paper. 1 to k represents all neighbors. 
        '''
        # self.model.schedule.agents is a list containing all other agents.
        self.nextOpinion = self.opinion
        
        # This calculates the next opinion based off the formula
        for other in self.neighbors: #Other is just a number.
            difference = self.opinion - self.model.schedule.agents[other].opinion
            if difference == 0: #Don't calculate for the same node. Unsure what to do if there are other nodes of the same opinion, probably doesn't matter at this point
                pass;
            else:
                #The negative is in the potential function now.
                self.nextOpinion += (ALPHA / 2) * self.potential(abs(difference)) * (difference / abs(difference))

        # Clamp function
        if self.nextOpinion > 1:
            self.nextOpinion = 1
        elif self.nextOpinion < 0:
            self.nextOpinion = 0
        

    def advance(self):
        self.opinion = self.nextOpinion
        self.nextOpinion = None

class OpinionModel(Model):
    '''A model with some number of agents'''
    def __init__(self, N):
        self.num_agents = N
        self.schedule = SimultaneousActivation(self)
        #Create agents
        for i in range(self.num_agents):
            #neighbors = [random.randint(0, N-1) for i in range((N + 3) // 4)] #So that nodes don't have 0 neighbors...
            neighbors = [i for i in range(N)]
            a = OpinionAgent(i, self, neighbors, potentials.gaussian())
            self.schedule.add(a)

        self.datacollector = DataCollector(
                agent_reporters = {"Opinion": lambda a: a.opinion}
        )
        
    def step(self):
        '''Advance the model one step'''
        self.datacollector.collect(self)
        self.schedule.step()
